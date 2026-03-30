"""Audit trail router — endpoints for audit log, verification, and export."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.db.audit_repository import (
    append_entry,
    find_entry_by_file_hash,
    get_all_entries_ordered,
    list_entries,
)
from backend.db.database import get_db
from backend.engine.audit_engine import verify_chain, verify_file_hash
from backend.models.audit_schemas import (
    AuditEntrySchema,
    AuditExportResponse,
    AuditLogResponse,
    AuditVerifyResponse,
    ChainVerifyResponse,
)

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/log", response_model=AuditLogResponse)
def get_audit_log(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    event_type: str | None = Query(None),
    db: Session = Depends(get_db),
) -> AuditLogResponse:
    """Paginated audit log query."""
    entries, total = list_entries(db, page=page, page_size=page_size, event_type=event_type)
    return AuditLogResponse(
        items=[AuditEntrySchema.model_validate(e) for e in entries],
        page=page,
        page_size=page_size,
        total=total,
    )


@router.get("/verify/{file_hash}", response_model=AuditVerifyResponse)
def verify_file(
    file_hash: str,
    current_hash: str = Query(..., description="Current hash of the file to verify"),
    db: Session = Depends(get_db),
) -> AuditVerifyResponse:
    """Verify a file hash against the stored upload hash."""
    entry = find_entry_by_file_hash(db, file_hash)
    if not entry:
        raise HTTPException(status_code=404, detail="No upload entry found for this file hash")
    result = verify_file_hash(entry.file_hash, current_hash)
    return AuditVerifyResponse(**result)


@router.get("/chain-verify", response_model=ChainVerifyResponse)
def chain_verify(db: Session = Depends(get_db)) -> ChainVerifyResponse:
    """Full chain verification — recompute all hashes in sequence."""
    entries = get_all_entries_ordered(db)
    entry_dicts = [
        {
            "id": e.id,
            "event_type": e.event_type,
            "timestamp": e.timestamp.isoformat(),
            "file_name": e.file_name,
            "file_hash": e.file_hash,
            "action_detail": e.action_detail,
            "previous_entry_hash": e.previous_entry_hash,
            "entry_hash": e.entry_hash,
        }
        for e in entries
    ]
    result = verify_chain(entry_dicts)
    return ChainVerifyResponse(**result)


@router.get("/export")
def export_audit(
    format: str = Query("json", pattern="^(json|pdf)$"),
    db: Session = Depends(get_db),
):
    """Export the full audit log with chain verification.

    The export action itself is logged as an audit entry.

    Query params:
        format: "json" (default) or "pdf"
    """
    # Get all entries for export
    entries = get_all_entries_ordered(db)
    entry_dicts = [
        {
            "id": e.id,
            "event_type": e.event_type,
            "timestamp": e.timestamp.isoformat(),
            "file_name": e.file_name,
            "file_hash": e.file_hash,
            "action_detail": e.action_detail,
            "previous_entry_hash": e.previous_entry_hash,
            "entry_hash": e.entry_hash,
        }
        for e in entries
    ]

    # Verify chain
    chain_result = verify_chain(entry_dicts)

    # Log the export action itself
    append_entry(
        db,
        event_type="export",
        action_detail=f"Audit log exported in {format} format",
    )

    if format == "pdf":
        try:
            from backend.engine.report_engine import generate_audit_report
            pdf_bytes = generate_audit_report(entry_dicts, chain_result)
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={
                    "Content-Disposition": 'inline; filename="audit_report.pdf"'
                },
            )
        except ImportError:
            # Fall through to JSON if WeasyPrint is not installed
            pass

    # Build JSON response (default or fallback)
    exported_at = datetime.now(timezone.utc)
    return AuditExportResponse(
        entries=[AuditEntrySchema.model_validate(e) for e in entries],
        chain_verification=ChainVerifyResponse(**chain_result),
        exported_at=exported_at,
    )
