"""Sigma analysis endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.engine.sigma_engine import calculate_batch
from backend.models.sigma_models import SigmaRecord
from backend.models.sigma_schemas import (
    SigmaCalculateRequest,
    SigmaCalculateResponse,
    SigmaHistoryEntry,
    SigmaHistoryResponse,
    SigmaResult,
)

router = APIRouter(prefix="/sigma", tags=["sigma"])


@router.post("/calculate", response_model=SigmaCalculateResponse)
def calculate_sigma(request: SigmaCalculateRequest, db: Session = Depends(get_db)):
    """Calculate Sigma scores for a batch of assays."""
    raw_inputs = [item.model_dump() for item in request.inputs]
    results = calculate_batch(raw_inputs)

    # Persist to history
    for r in results:
        record = SigmaRecord(
            assay=r["assay"],
            tea_percent=next(i.tea_percent for i in request.inputs if i.assay == r["assay"]),
            bias_percent=next(i.bias_percent for i in request.inputs if i.assay == r["assay"]),
            cv_percent=next(i.cv_percent for i in request.inputs if i.assay == r["assay"]),
            sigma_score=r["sigma_score"],
            classification=r["classification"],
        )
        db.add(record)
    db.commit()

    return SigmaCalculateResponse(results=[SigmaResult(**r) for r in results])


@router.get("/history", response_model=SigmaHistoryResponse)
def get_sigma_history(assay: str = Query(...), db: Session = Depends(get_db)):
    """Get historical Sigma trend for an assay."""
    records = (
        db.query(SigmaRecord)
        .filter(SigmaRecord.assay == assay)
        .order_by(SigmaRecord.calculated_at.desc())
        .all()
    )

    entries = [
        SigmaHistoryEntry(
            assay=r.assay,
            sigma_score=r.sigma_score,
            classification=r.classification,
            calculated_at=r.calculated_at.isoformat(),
        )
        for r in records
    ]
    return SigmaHistoryResponse(assay=assay, entries=entries)


@router.get("/report")
def get_sigma_report(db: Session = Depends(get_db)):
    """Generate Sigma report PDF from all stored sigma records.

    Returns PDF with content-type application/pdf.
    """
    records = (
        db.query(SigmaRecord)
        .order_by(SigmaRecord.calculated_at.desc())
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail="No sigma records found")

    sigma_results = [
        {
            "assay": r.assay,
            "tea_percent": r.tea_percent,
            "bias_percent": r.bias_percent,
            "cv_percent": r.cv_percent,
            "sigma_score": r.sigma_score,
            "classification": r.classification,
            "recommended_rules": _get_recommended_rules(r.sigma_score),
            "nmedx_x": round(r.bias_percent / r.tea_percent, 4) if r.tea_percent else 0,
            "nmedx_y": round(r.cv_percent / r.tea_percent, 4) if r.tea_percent else 0,
            "notes": _get_sigma_notes(r.sigma_score),
        }
        for r in records
    ]

    try:
        from backend.engine.report_engine import generate_sigma_report
        pdf_bytes = generate_sigma_report(sigma_results)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'inline; filename="sigma_report.pdf"'
            },
        )
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="PDF generation unavailable (WeasyPrint not installed)",
        )


def _get_recommended_rules(sigma_score: float) -> list[str]:
    """Get recommended rules for a sigma score (mirrors sigma_engine logic)."""
    from backend.engine.sigma_engine import get_recommended_rules
    rules, _ = get_recommended_rules(sigma_score)
    return rules


def _get_sigma_notes(sigma_score: float) -> str | None:
    """Get notes for a sigma score (mirrors sigma_engine logic)."""
    from backend.engine.sigma_engine import get_recommended_rules
    _, notes = get_recommended_rules(sigma_score)
    return notes
