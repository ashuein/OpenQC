"""Pydantic schemas for audit trail API requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class AuditEntrySchema(BaseModel):
    id: int
    timestamp: datetime
    event_type: str
    file_name: str | None = None
    file_hash: str | None = None
    action_detail: str
    previous_entry_hash: str
    entry_hash: str

    model_config = {"from_attributes": True}


class AuditLogResponse(BaseModel):
    items: list[AuditEntrySchema]
    page: int
    page_size: int
    total: int


class AuditVerifyResponse(BaseModel):
    match: bool
    stored_hash: str
    current_hash: str


class ChainVerifyResponse(BaseModel):
    valid: bool
    first_invalid_id: int | None = None
    entries_checked: int


class AuditExportResponse(BaseModel):
    entries: list[AuditEntrySchema]
    chain_verification: ChainVerifyResponse
    exported_at: datetime
