"""CRUD operations for QC runs and data points."""

from __future__ import annotations

import json
import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.models.qc_models import QCDataPoint, QCRun


def create_run(db: Session, run_data: dict) -> QCRun:
    """Insert a new QC run record and return it."""
    run = QCRun(
        id=run_data.get("id", str(uuid.uuid4())),
        file_name=run_data["file_name"],
        file_hash=run_data["file_hash"],
        instrument=run_data["instrument"],
        assay=run_data["assay"],
        channel=run_data.get("channel"),
        reagent_lot_id=run_data.get("reagent_lot_id"),
        control_lot_id=run_data.get("control_lot_id"),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def get_run(db: Session, run_id: str) -> QCRun | None:
    """Fetch a single QC run by ID (or ``None`` if not found)."""
    return db.query(QCRun).filter(QCRun.id == run_id).first()


def list_runs(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    assay: str | None = None,
) -> tuple[list[QCRun], int]:
    """Return a page of QC runs and the total count.

    Parameters
    ----------
    page : int
        1-based page number.
    page_size : int
        Number of runs per page.
    assay : str | None
        Optional filter by assay name.

    Returns
    -------
    tuple[list[QCRun], int]
        (runs, total_count)
    """
    query = db.query(QCRun)
    if assay:
        query = query.filter(QCRun.assay == assay)

    total = query.count()
    runs = (
        query.order_by(QCRun.uploaded_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return runs, total


def delete_run(db: Session, run_id: str) -> bool:
    """Delete a QC run and its data points.  Returns True if found."""
    run = get_run(db, run_id)
    if run is None:
        return False
    db.delete(run)
    db.commit()
    return True


def add_data_points(
    db: Session, run_id: str, points: list[dict]
) -> list[QCDataPoint]:
    """Bulk-insert data points for a run."""
    db_points: list[QCDataPoint] = []
    for pt in points:
        violations_val = pt.get("violations")
        if isinstance(violations_val, list):
            violations_val = json.dumps(violations_val)

        dp = QCDataPoint(
            id=str(uuid.uuid4()),
            run_id=run_id,
            sequence_index=pt["sequence_index"],
            control_level=pt["control_level"],
            ct_value=pt["ct_value"],
            mean=pt.get("mean"),
            sd=pt.get("sd"),
            z_score=pt.get("z_score"),
            violations=violations_val,
        )
        db.add(dp)
        db_points.append(dp)

    db.commit()
    for dp in db_points:
        db.refresh(dp)
    return db_points


def get_run_history(
    db: Session,
    assay: str,
    channel: str | None,
    control_level: str,
    reagent_lot_id: str | None = None,
    control_lot_id: str | None = None,
    exclude_run_id: str | None = None,
    before: "datetime | None" = None,
    limit: int = 20,
) -> list[QCDataPoint]:
    """Retrieve historical data points for a specific assay/control combination.

    Used to populate the z-score history for rules like 2-2s, 4-1s, 10x.

    Parameters
    ----------
    exclude_run_id : str | None
        Run ID to exclude from results (typically the current run).
    before : datetime | None
        Only include points from runs uploaded before this timestamp.
    """
    query = (
        db.query(QCDataPoint)
        .join(QCRun)
        .filter(
            QCRun.assay == assay,
            QCDataPoint.control_level == control_level,
        )
    )

    # Use IS NULL matching when stream keys are None, not wildcard
    if channel is not None:
        query = query.filter(QCRun.channel == channel)
    else:
        query = query.filter(QCRun.channel.is_(None))
    if reagent_lot_id is not None:
        query = query.filter(QCRun.reagent_lot_id == reagent_lot_id)
    else:
        query = query.filter(QCRun.reagent_lot_id.is_(None))
    if control_lot_id is not None:
        query = query.filter(QCRun.control_lot_id == control_lot_id)
    else:
        query = query.filter(QCRun.control_lot_id.is_(None))
    if exclude_run_id is not None:
        query = query.filter(QCRun.id != exclude_run_id)
    if before is not None:
        query = query.filter(QCRun.uploaded_at < before)

    # Order oldest-first so callers get correct chronological sequence
    # for consecutive Westgard rule evaluation.
    return (
        query.order_by(QCRun.uploaded_at.asc(), QCDataPoint.sequence_index.asc())
        .limit(limit)
        .all()
    )
