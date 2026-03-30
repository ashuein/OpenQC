"""SQLAlchemy ORM models for assay validation datasets and runs."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from backend.db.database import Base


class ValidationDataset(Base):
    """Stores an uploaded validation dataset and its raw data."""

    __tablename__ = "validation_datasets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = Column(String, nullable=False)
    file_hash = Column(String(64), nullable=False)  # SHA-256
    validation_type = Column(String, nullable=False)
    row_count = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    raw_data = Column(Text, nullable=False)  # JSON text


class ValidationRun(Base):
    """Stores results of a single validation calculation run."""

    __tablename__ = "validation_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dataset_id = Column(
        String, ForeignKey("validation_datasets.id"), nullable=False
    )
    overall_status = Column(String, nullable=False)  # "pass"|"fail"
    results_json = Column(Text, nullable=False)  # JSON text
    acceptance_criteria_json = Column(Text, nullable=False)  # JSON text
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
