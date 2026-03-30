"""SQLAlchemy ORM model for app settings."""
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Text
from backend.db.database import Base


class AppSetting(Base):
    __tablename__ = "app_settings"

    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)
