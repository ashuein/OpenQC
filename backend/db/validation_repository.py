"""CRUD operations for validation datasets and runs."""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.validation_models import ValidationDataset, ValidationRun


def create_dataset(db: Session, data: dict) -> ValidationDataset:
    """Insert a new ValidationDataset row and return it."""
    dataset = ValidationDataset(**data)
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset


def get_dataset(db: Session, dataset_id: str) -> ValidationDataset | None:
    """Fetch a single dataset by ID, or None if not found."""
    return db.query(ValidationDataset).filter_by(id=dataset_id).first()


def create_validation_run(db: Session, data: dict) -> ValidationRun:
    """Insert a new ValidationRun row and return it."""
    run = ValidationRun(**data)
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_validation_run(db: Session, run_id: str) -> ValidationRun | None:
    """Fetch a single validation run by ID, or None if not found."""
    return db.query(ValidationRun).filter_by(id=run_id).first()
