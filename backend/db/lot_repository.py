"""Lot registry repository -- CRUD for reagent and control lots."""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from backend.models.lot_models import ReagentLot, ControlLot


def create_reagent_lot(db: Session, data: dict) -> ReagentLot:
    """Create a reagent lot. Raises ValueError if active duplicate exists for same assay."""
    existing = db.query(ReagentLot).filter(
        and_(
            ReagentLot.assay_name == data["assay_name"],
            ReagentLot.lot_number == data["lot_number"],
            ReagentLot.status == "active",
        )
    ).first()
    if existing:
        raise ValueError(
            f"Active reagent lot {data['lot_number']} already exists for {data['assay_name']}"
        )
    lot = ReagentLot(**data)
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


def list_reagent_lots(db: Session) -> list[ReagentLot]:
    return db.query(ReagentLot).order_by(ReagentLot.created_at.desc()).all()


def get_reagent_lot(db: Session, lot_id: str) -> ReagentLot | None:
    return db.query(ReagentLot).filter(ReagentLot.id == lot_id).first()


def update_reagent_lot_status(db: Session, lot_id: str, status: str) -> ReagentLot | None:
    lot = get_reagent_lot(db, lot_id)
    if lot:
        lot.status = status
        db.commit()
        db.refresh(lot)
    return lot


def create_control_lot(db: Session, data: dict) -> ControlLot:
    """Create a control lot. Raises ValueError if active duplicate exists for same control."""
    existing = db.query(ControlLot).filter(
        and_(
            ControlLot.control_name == data["control_name"],
            ControlLot.lot_number == data["lot_number"],
            ControlLot.status == "active",
        )
    ).first()
    if existing:
        raise ValueError(
            f"Active control lot {data['lot_number']} already exists for {data['control_name']}"
        )
    lot = ControlLot(**data)
    db.add(lot)
    db.commit()
    db.refresh(lot)
    return lot


def list_control_lots(db: Session) -> list[ControlLot]:
    return db.query(ControlLot).order_by(ControlLot.created_at.desc()).all()


def get_control_lot(db: Session, lot_id: str) -> ControlLot | None:
    return db.query(ControlLot).filter(ControlLot.id == lot_id).first()


def update_control_lot_status(db: Session, lot_id: str, status: str) -> ControlLot | None:
    lot = get_control_lot(db, lot_id)
    if lot:
        lot.status = status
        db.commit()
        db.refresh(lot)
    return lot
