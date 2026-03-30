"""QC module router -- upload, analyze, list, get, delete QC runs."""

from __future__ import annotations

import json

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.qc_repository import (
    add_data_points,
    create_run,
    delete_run,
    get_run,
    list_runs,
)
from backend.engine.westgard_rules import evaluate_rules
from backend.models.qc_schemas import (
    PaginatedRuns,
    QCAnalysisResult,
    QCDataPointSchema,
    QCRunResponse,
    QCRunSummary,
)
from backend.utils.hasher import hash_file

router = APIRouter(prefix="/qc", tags=["qc"])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _orm_point_to_schema(dp) -> QCDataPointSchema:
    """Convert an ORM QCDataPoint to a Pydantic schema."""
    violations: list[str] = []
    if dp.violations:
        try:
            violations = json.loads(dp.violations)
        except (json.JSONDecodeError, TypeError):
            violations = []

    return QCDataPointSchema(
        cycle=dp.sequence_index,
        control_level=dp.control_level,
        ct_value=dp.ct_value,
        mean=dp.mean,
        sd=dp.sd,
        z_score=dp.z_score,
        violations=violations,
    )


def _orm_run_to_response(run) -> QCRunResponse:
    """Convert an ORM QCRun to the full response schema."""
    return QCRunResponse(
        id=run.id,
        uploaded_at=run.uploaded_at,
        file_name=run.file_name,
        file_hash=run.file_hash,
        instrument=run.instrument,
        assay=run.assay,
        channel=run.channel,
        reagent_lot_id=run.reagent_lot_id,
        control_lot_id=run.control_lot_id,
        data_points=[_orm_point_to_schema(dp) for dp in run.data_points],
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/upload", response_model=QCRunResponse)
async def upload_qc_run(
    file: UploadFile = File(...),
    instrument: str = Form(...),
    assay: str = Form(...),
    channel: str | None = Form(None),
    reagent_lot_id: str | None = Form(None),
    control_lot_id: str | None = Form(None),
    db: Session = Depends(get_db),
) -> QCRunResponse:
    """Upload a QC file, parse it, and store the run + data points."""
    file_bytes = await file.read()
    file_hash_val = hash_file(file_bytes)
    file_name = file.filename or "unknown"

    # Try parsers in priority order
    from backend.parsers.quantstudio_parser import QuantStudioParser
    from backend.parsers.generic_parser import GenericParser

    parsers = [QuantStudioParser(), GenericParser()]
    metadata = {"filename": file_name, "file_bytes": file_bytes}

    parsed: dict | None = None
    for parser in parsers:
        if parser.can_handle(metadata):
            parsed = parser.parse(file_bytes)
            break

    if parsed is None or not parsed.get("rows"):
        raise HTTPException(status_code=400, detail="No data points could be parsed from the uploaded file.")

    # Create the run record
    run = create_run(db, {
        "file_name": file_name,
        "file_hash": file_hash_val,
        "instrument": instrument,
        "assay": assay,
        "channel": channel,
        "reagent_lot_id": reagent_lot_id,
        "control_lot_id": control_lot_id,
    })

    # Convert parsed rows to data point dicts
    point_dicts = []
    for idx, row in enumerate(parsed["rows"]):
        point_dicts.append({
            "sequence_index": idx,
            "control_level": row["control_level"],
            "ct_value": row["ct_value"],
        })

    add_data_points(db, run.id, point_dicts)

    # Refresh to include data_points
    db.refresh(run)
    return _orm_run_to_response(run)


@router.post("/analyze", response_model=QCAnalysisResult)
def analyze_qc_run(
    body: dict,
    db: Session = Depends(get_db),
) -> QCAnalysisResult:
    """Run Westgard analysis on a stored QC run."""
    run_id = body.get("run_id")
    if not run_id:
        raise HTTPException(status_code=400, detail="run_id is required")

    run = get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    # Build points list for the engine
    points: list[dict] = []
    for dp in sorted(run.data_points, key=lambda d: d.sequence_index):
        points.append({
            "ct_value": dp.ct_value,
            "mean": dp.mean if dp.mean is not None else dp.ct_value,
            "sd": dp.sd if dp.sd is not None else 1.0,
            "control_level": dp.control_level,
            "sequence_index": dp.sequence_index,
        })

    # Determine if R-4s should be enabled (multi-control)
    control_levels = {dp.control_level for dp in run.data_points}
    assay_config = {
        "r4s_enabled": len(control_levels) > 1,
        "controls_per_run": len(control_levels),
    }

    result = evaluate_rules(points, assay_config)

    # Update data points in DB with computed z-scores and violations
    for ep in result["evaluated_points"]:
        for dp in run.data_points:
            if dp.sequence_index == ep["cycle"]:
                dp.z_score = ep["z_score"]
                dp.violations = json.dumps(ep["violations"]) if ep["violations"] else None
                break
    db.commit()

    return QCAnalysisResult(
        run_id=run_id,
        run_status=result["run_status"],
        first_reject_rule=result["first_reject_rule"],
        violations=result["violations"],
        warning_rules=result["warning_rules"],
        reject_rules=result["reject_rules"],
        evaluated_points=[QCDataPointSchema(**ep) for ep in result["evaluated_points"]],
        summary_stats=result["summary_stats"],
    )


@router.get("/runs", response_model=PaginatedRuns)
def get_qc_runs(
    assay: str | None = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
) -> PaginatedRuns:
    """Return a paginated list of QC runs."""
    runs, total = list_runs(db, page=page, page_size=page_size, assay=assay)

    items = []
    for run in runs:
        # Compute run_status and violation_count from stored data
        violation_count = 0
        has_reject = False
        has_warning = False
        for dp in run.data_points:
            if dp.violations:
                try:
                    v = json.loads(dp.violations)
                    violation_count += len(v)
                    for rule in v:
                        if rule == "1-2s":
                            has_warning = True
                        else:
                            has_reject = True
                except (json.JSONDecodeError, TypeError):
                    pass

        if has_reject:
            run_status = "reject"
        elif has_warning:
            run_status = "warning"
        else:
            run_status = "pass"

        items.append(QCRunSummary(
            id=run.id,
            uploaded_at=run.uploaded_at,
            file_name=run.file_name,
            assay=run.assay,
            instrument=run.instrument,
            run_status=run_status,
            violation_count=violation_count,
        ))

    return PaginatedRuns(items=items, page=page, page_size=page_size, total=total)


@router.get("/run/{run_id}", response_model=QCRunResponse)
def get_qc_run(
    run_id: str,
    db: Session = Depends(get_db),
) -> QCRunResponse:
    """Return the full details of a single QC run."""
    run = get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return _orm_run_to_response(run)


@router.delete("/run/{run_id}")
def delete_qc_run(
    run_id: str,
    db: Session = Depends(get_db),
) -> dict:
    """Delete a QC run and all its data points."""
    deleted = delete_run(db, run_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return {"detail": f"Run {run_id} deleted"}


@router.get("/report/{run_id}")
def get_qc_report(
    run_id: str,
    db: Session = Depends(get_db),
):
    """Generate QC run report as PDF.

    Fetches run data and re-runs Westgard analysis to produce the report.
    Returns PDF with content-type application/pdf.
    """
    run = get_run(db, run_id)
    if run is None:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")

    # Build points list for the engine
    points: list[dict] = []
    for dp in sorted(run.data_points, key=lambda d: d.sequence_index):
        points.append({
            "ct_value": dp.ct_value,
            "mean": dp.mean if dp.mean is not None else dp.ct_value,
            "sd": dp.sd if dp.sd is not None else 1.0,
            "control_level": dp.control_level,
            "sequence_index": dp.sequence_index,
        })

    # Determine if R-4s should be enabled (multi-control)
    control_levels = {dp.control_level for dp in run.data_points}
    assay_config = {
        "r4s_enabled": len(control_levels) > 1,
        "controls_per_run": len(control_levels),
    }

    result = evaluate_rules(points, assay_config)

    # Prepare run_data dict
    run_data = {
        "id": run.id,
        "assay": run.assay,
        "instrument": run.instrument,
        "uploaded_at": run.uploaded_at.isoformat() if run.uploaded_at else "",
        "reagent_lot_id": run.reagent_lot_id,
        "control_lot_id": run.control_lot_id,
        "file_name": run.file_name,
        "file_hash": run.file_hash,
    }

    # Prepare analysis_data — map evaluated_points to template format
    evaluated_points = []
    for ep in result["evaluated_points"]:
        evaluated_points.append({
            "sequence_index": ep["cycle"],
            "control_level": ep["control_level"],
            "ct_value": ep["ct_value"],
            "mean": ep["mean"],
            "sd": ep["sd"],
            "z_score": ep["z_score"],
            "violations": ep["violations"],
        })

    # Map violations to template format (add ct_value)
    violations = []
    for v in result["violations"]:
        # Find matching point for ct_value
        ct_val = None
        for ep in result["evaluated_points"]:
            if ep["cycle"] == v["sequence_index"]:
                ct_val = ep["ct_value"]
                break
        violations.append({
            "sequence_index": v["sequence_index"],
            "control_level": v["control_level"],
            "ct_value": ct_val,
            "z_score": v["z_score"],
            "rules": v["rules"],
        })

    analysis_data = {
        "run_status": result["run_status"],
        "first_reject_rule": result["first_reject_rule"],
        "violations": violations,
        "summary_stats": result["summary_stats"],
        "evaluated_points": evaluated_points,
    }

    try:
        from backend.engine.report_engine import generate_qc_report
        pdf_bytes = generate_qc_report(run_data, analysis_data)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="qc_report_{run_id}.pdf"'
            },
        )
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="PDF generation unavailable (WeasyPrint not installed)",
        )
