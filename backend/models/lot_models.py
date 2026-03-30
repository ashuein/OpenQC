"""SQLAlchemy ORM models for lot tracking."""
import uuid
from datetime import date, datetime, timezone
from sqlalchemy import Column, String, Float, Date, DateTime
from backend.db.database import Base


class ReagentLot(Base):
    __tablename__ = "reagent_lots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assay_name = Column(String, nullable=False)
    lot_number = Column(String, nullable=False)
    expiry_date = Column(Date, nullable=True)
    open_date = Column(Date, nullable=True)
    status = Column(String, default="active", nullable=False)  # active|inactive|expired
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class ControlLot(Base):
    __tablename__ = "control_lots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    control_name = Column(String, nullable=False)
    manufacturer = Column(String, nullable=True)
    lot_number = Column(String, nullable=False)
    assigned_mean = Column(Float, nullable=True)
    assigned_sd = Column(Float, nullable=True)
    expiry_date = Column(Date, nullable=True)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
