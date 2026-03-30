"""Audit trail repository — database CRUD for audit entries."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.engine.audit_engine import compute_entry_hash
from backend.models.audit_models import AuditEntry
from backend.utils.hasher import GENESIS_HASH


def get_last_entry(db: Session) -> AuditEntry | None:
    """Get the most recent audit entry."""
    return db.query(AuditEntry).order_by(AuditEntry.id.desc()).first()


def append_entry(
    db: Session,
    event_type: str,
    action_detail: str,
    file_name: str | None = None,
    file_hash: str | None = None,
) -> AuditEntry:
    """Append a new entry to the audit chain."""
    last = get_last_entry(db)
    previous_hash = last.entry_hash if last else GENESIS_HASH

    timestamp = datetime.now(timezone.utc)
    entry_hash = compute_entry_hash(
        event_type,
        timestamp.isoformat(),
        file_name,
        file_hash,
        action_detail,
        previous_hash,
    )

    entry = AuditEntry(
        timestamp=timestamp,
        event_type=event_type,
        file_name=file_name,
        file_hash=file_hash,
        action_detail=action_detail,
        previous_entry_hash=previous_hash,
        entry_hash=entry_hash,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def list_entries(
    db: Session,
    page: int = 1,
    page_size: int = 50,
    event_type: str | None = None,
) -> tuple[list[AuditEntry], int]:
    """Paginated audit log query."""
    query = db.query(AuditEntry)
    if event_type:
        query = query.filter(AuditEntry.event_type == event_type)
    total = query.count()
    entries = (
        query.order_by(AuditEntry.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return entries, total


def get_all_entries_ordered(db: Session) -> list[AuditEntry]:
    """Get all entries in chain order (ascending ID) for verification."""
    return db.query(AuditEntry).order_by(AuditEntry.id.asc()).all()


def find_entry_by_file_hash(db: Session, file_hash: str) -> AuditEntry | None:
    """Find an audit entry by stored file hash."""
    return (
        db.query(AuditEntry)
        .filter(AuditEntry.file_hash == file_hash, AuditEntry.event_type == "upload")
        .first()
    )
