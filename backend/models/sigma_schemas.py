"""Pydantic schemas for Sigma analysis API."""
from pydantic import BaseModel, field_validator


class SigmaInput(BaseModel):
    assay: str
    tea_percent: float
    bias_percent: float
    cv_percent: float

    @field_validator("cv_percent")
    @classmethod
    def cv_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("cv_percent must be > 0")
        return v

    @field_validator("tea_percent")
    @classmethod
    def tea_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("tea_percent must be > 0")
        return v

    @field_validator("bias_percent")
    @classmethod
    def bias_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("bias_percent must be >= 0")
        return v


class SigmaResult(BaseModel):
    assay: str
    sigma_score: float
    classification: str
    recommended_rules: list[str]
    nmedx_x: float
    nmedx_y: float
    notes: str | None = None


class SigmaCalculateRequest(BaseModel):
    inputs: list[SigmaInput]


class SigmaCalculateResponse(BaseModel):
    results: list[SigmaResult]


class SigmaHistoryEntry(BaseModel):
    assay: str
    sigma_score: float
    classification: str
    calculated_at: str  # ISO 8601


class SigmaHistoryResponse(BaseModel):
    assay: str
    entries: list[SigmaHistoryEntry]
