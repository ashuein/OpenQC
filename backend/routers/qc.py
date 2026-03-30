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
    get_run_history,
    list_runs,
)
from backend.db.lot_repository import get_control_lot
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


def _resolve_mean_sd(dp, run, db: Session) -> tuple[float, float]:
    """Resolve mean and SD for a data point, falling back to control lot."""
    mu = dp.mean if hasattr(dp, 'mean') else dp.get("mean")
    sigma = dp.sd if hasattr(dp, 'sd') else dp.get("sd")
    lot_id = run.control_lot_id if hasattr(run, 'control_lot_id') else run.get("control_lot_id")

    if mu is None or sigma is None:
        if lot_id:
            lot = get_control_lot(db, lot_id)
            if lot:
                mu = mu if mu is not None else lot.assigned_mean
                sigma = sigma if sigma is not None else lot.assigned_sd

    return mu, sigma


def _build_analysis_points(run, db: Session) -> tuple[list[dict], dict]:
    """Build the full point list (history + current) and assay config for Westgard analysis.

    Returns (all_points, assay_config). History points have _is_history=True.
    """
    control_levels = {dp.control_level for dp in run.data_points}
    assay_config = {
        "r4s_enabled": len(control_levels) > 1,
        "controls_per_run": len(control_levels),
    }

    all_points: list[dict] = []

    # Prepend cross-run history per control level.
    # Exclude the current run at the DB level so the limit is not wasted,
    # and bound to runs uploaded before the current run for temporal consistency.
    for level in sorted(control_levels):
        history = get_run_history(
            db, assay=run.assay, channel=run.channel,
            control_level=level,
            reagent_lot_id=run.reagent_lot_id,
            control_lot_id=run.control_lot_id,
            exclude_run_id=run.id,
            before=run.uploaded_at,
            limit=20,
        )
        for hp in history:  # already oldest-first from DB
            mu, sigma = _resolve_mean_sd(hp, run, db)
            if mu is None or sigma is None:
                continue  # Skip legacy points without resolvable stats
            all_points.append({
                "ct_value": hp.ct_value,
                "mean": mu,
                "sd": sigma,
                "control_level": hp.control_level,
                "sequence_index": hp.sequence_index,
                "_is_history": True,
            })

    # Add current run points
    for dp in sorted(run.data_points, key=lambda d: d.sequence_index):
        mu, sigma = _resolve_mean_sd(dp, run, db)
        if mu is None or sigma is None:
            raise HTTPException(
                status_code=400,
                detail=f"Data point at index {dp.sequence_index} has no mean/SD. "
                       "Upload a file with Ct Mean/SD columns or assign a control lot with mean/SD.",
            )
        all_points.append({
            "ct_value": dp.ct_value,
            "mean": mu,
            "sd": sigma,
            "control_level": dp.control_level,
            "sequence_index": dp.sequence_index,
            "_is_history": False,
        })

    return all_points, assay_config


def _filter_analysis_result(result: dict) -> dict:
    """Filter evaluate_rules output to only current-run points and recompute stats."""
    current_points = [ep for ep in result["evaluated_points"] if not ep.get("_is_history", False)]
    current_violations = [v for v in result["violations"] if not v.get("_is_history", False)]

    # Recompute run status from current-run violations only
    reject_rules: list[str] = []
    warning_rules: list[str] = []
    first_reject = None
    for v in current_violations:
        for rule in v["rules"]:
            if rule == "1-2s":
                if rule not in warning_rules:
                    warning_rules.append(rule)
            else:
                if rule not in reject_rules:
                    reject_rules.append(rule)
                if first_reject is None:
                    first_reject = rule

    if reject_rules:
        run_status = "reject"
    elif warning_rules:
        run_status = "warning"
    else:
        run_status = "pass"

    # Recompute summary stats from current-run points only
    summary_stats: dict = {}
    all_z = [ep["z_score"] for ep in current_points]
    if all_z:
        summary_stats["mean_z"] = round(sum(all_z) / len(all_z), 6)
        summary_stats["max_z"] = round(max(all_z), 6)
        summary_stats["min_z"] = round(min(all_z), 6)
        summary_stats["point_count"] = len(all_z)
    if current_points:
        summary_stats["mean"] = current_points[0]["mean"]
        summary_stats["sd"] = current_points[0]["sd"]

    return {
        "run_status": run_status,
        "first_reject_rule": first_reject,
        "violations": current_violations,
        "warning_rules": warning_rules,
        "reject_rules": reject_rules,
        "evaluated_points": current_points,
        "summary_stats": summary_stats,
    }


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
            "mean": row.get("mean"),
            "sd": row.get("sd"),
        })

    add_data_points(db, run.id, point_dicts)

    # Audit entry for the upload
    from backend.db.audit_repository import append_entry

    append_entry(
        db,
        event_type="upload",
        action_detail=f"QC file uploaded: {file_name} for assay {assay}",
        file_name=file_name,
        file_hash=file_hash_val,
    )

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

    all_points, assay_config = _build_analysis_points(run, db)
    raw_result = evaluate_rules(all_points, assay_config)
    result = _filter_analysis_result(raw_result)

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

    # Use the same history-aware analysis as /qc/analyze
    all_points, assay_config = _build_analysis_points(run, db)
    raw_result = evaluate_rules(all_points, assay_config)
    result = _filter_analysis_result(raw_result)

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
