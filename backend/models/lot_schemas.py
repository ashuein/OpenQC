"""Pydantic schemas for Lot Tracker API."""
from pydantic import BaseModel
from datetime import date, datetime


class ReagentLotCreate(BaseModel):
    assay_name: str
    lot_number: str
    expiry_date: date | None = None
    open_date: date | None = None


class ReagentLotResponse(BaseModel):
    id: str
    assay_name: str
    lot_number: str
    expiry_date: date | None = None
    open_date: date | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ControlLotCreate(BaseModel):
    control_name: str
    manufacturer: str | None = None
    lot_number: str
    assigned_mean: float | None = None
    assigned_sd: float | None = None
    expiry_date: date | None = None


class ControlLotResponse(BaseModel):
    id: str
    control_name: str
    manufacturer: str | None = None
    lot_number: str
    assigned_mean: float | None = None
    assigned_sd: float | None = None
    expiry_date: date | None = None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
