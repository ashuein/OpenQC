"""SQLAlchemy ORM model for audit trail entries."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.db.database import Base


class AuditEntry(Base):
    __tablename__ = "audit_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    event_type = Column(String, nullable=False)  # upload|view|export|lot_change|settings|rag_query
    file_name = Column(String, nullable=True)
    file_hash = Column(String(64), nullable=True)
    action_detail = Column(Text, nullable=False)
    previous_entry_hash = Column(String(64), nullable=False)
    entry_hash = Column(String(64), nullable=False)
