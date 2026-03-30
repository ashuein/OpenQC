"""SQLAlchemy ORM models for QC runs and data points."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from backend.db.database import Base


class QCRun(Base):
    __tablename__ = "qc_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    file_name = Column(String, nullable=False)
    file_hash = Column(String(64), nullable=False)  # SHA-256
    instrument = Column(String, nullable=False)
    assay = Column(String, nullable=False)
    channel = Column(String, nullable=True)
    reagent_lot_id = Column(String, nullable=True)
    control_lot_id = Column(String, nullable=True)

    data_points = relationship(
        "QCDataPoint", back_populates="run", cascade="all, delete-orphan"
    )


class QCDataPoint(Base):
    __tablename__ = "qc_data_points"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String, ForeignKey("qc_runs.id"), nullable=False)
    sequence_index = Column(Integer, nullable=False)
    control_level = Column(String, nullable=False)  # L1, L2, L3
    ct_value = Column(Float, nullable=False)
    mean = Column(Float, nullable=True)
    sd = Column(Float, nullable=True)
    z_score = Column(Float, nullable=True)
    violations = Column(Text, nullable=True)  # JSON string of rule codes

    run = relationship("QCRun", back_populates="data_points")
