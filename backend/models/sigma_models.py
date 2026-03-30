"""SQLAlchemy ORM model for Sigma history."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, String

from backend.db.database import Base


class SigmaRecord(Base):
    __tablename__ = "sigma_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    assay = Column(String, nullable=False, index=True)
    tea_percent = Column(Float, nullable=False)
    bias_percent = Column(Float, nullable=False)
    cv_percent = Column(Float, nullable=False)
    sigma_score = Column(Float, nullable=False)
    classification = Column(String, nullable=False)
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
