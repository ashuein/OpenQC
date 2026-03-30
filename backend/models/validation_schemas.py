"""Pydantic v2 API schemas for the Validation module."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class ValidationUploadResponse(BaseModel):
    """Response after uploading a validation dataset."""

    dataset_id: str
    file_name: str
    validation_type: str  # "lod"|"loq"|"precision_intra"|"precision_inter"|"linearity"
    row_count: int
    uploaded_at: datetime


class AcceptanceCriterion(BaseModel):
    """Single acceptance criterion for a validation metric."""

    metric: str
    threshold: float
    operator: str  # "lte" or "gte"


class ValidationRunRequest(BaseModel):
    """Request body for running validation calculations."""

    dataset_id: str
    acceptance_criteria: list[AcceptanceCriterion]


class ValidationMetric(BaseModel):
    """One metric from a validation run result."""

    metric: str
    value: float | None
    threshold: float | None = None
    operator: str | None = None
    status: str  # "pass"|"fail"|"not_evaluated"


class ValidationResult(BaseModel):
    """Full validation run result."""

    validation_id: str
    dataset_id: str
    validation_type: str
    overall_status: str  # "pass"|"fail"
    metrics: list[ValidationMetric]
    raw_summary: dict
    calculated_at: datetime
