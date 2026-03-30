"""Pydantic v2 API schemas for the QC module."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class QCDataPointSchema(BaseModel):
    """Schema for a single QC data point returned in API responses."""

    model_config = ConfigDict(from_attributes=True)

    cycle: int
    control_level: str
    ct_value: float
    mean: float | None = None
    sd: float | None = None
    z_score: float | None = None
    violations: list[str] = []


class QCRunUploadRequest(BaseModel):
    """Form metadata supplied alongside the uploaded file."""

    instrument: str
    assay: str
    channel: str | None = None
    reagent_lot_id: str | None = None
    control_lot_id: str | None = None


class QCRunResponse(BaseModel):
    """Full run record returned after upload or single-run lookup."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    uploaded_at: datetime
    file_name: str
    file_hash: str
    instrument: str
    assay: str
    channel: str | None = None
    reagent_lot_id: str | None = None
    control_lot_id: str | None = None
    data_points: list[QCDataPointSchema] = []


class QCRunSummary(BaseModel):
    """Lightweight run summary used in paginated list responses."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    uploaded_at: datetime
    file_name: str
    assay: str
    instrument: str
    run_status: str
    violation_count: int


class QCAnalysisResult(BaseModel):
    """Result of running Westgard analysis on a stored QC run."""

    run_id: str
    run_status: str  # "pass" | "warning" | "reject"
    first_reject_rule: str | None = None
    violations: list[dict] = []
    warning_rules: list[str] = []
    reject_rules: list[str] = []
    evaluated_points: list[QCDataPointSchema] = []
    summary_stats: dict = {}


class PaginatedRuns(BaseModel):
    """Paginated list of QC run summaries."""

    items: list[QCRunSummary]
    page: int
    page_size: int
    total: int
