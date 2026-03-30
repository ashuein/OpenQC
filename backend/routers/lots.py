"""Lots / reagent-lot and control-lot tracking router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.lot_repository import (
    create_control_lot,
    create_reagent_lot,
    list_control_lots,
    list_reagent_lots,
)
from backend.models.lot_schemas import (
    ControlLotCreate,
    ControlLotResponse,
    ReagentLotCreate,
    ReagentLotResponse,
)

router = APIRouter(prefix="/lots", tags=["lots"])


@router.get("/reagents", response_model=list[ReagentLotResponse])
def get_reagent_lots(db: Session = Depends(get_db)):
    """List all reagent lots ordered by most recent first."""
    return list_reagent_lots(db)


@router.post("/reagents", response_model=ReagentLotResponse, status_code=201)
def add_reagent_lot(body: ReagentLotCreate, db: Session = Depends(get_db)):
    """Register a new reagent lot. Returns 409 if an active duplicate exists."""
    try:
        return create_reagent_lot(db, body.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@router.get("/controls", response_model=list[ControlLotResponse])
def get_control_lots(db: Session = Depends(get_db)):
    """List all control lots ordered by most recent first."""
    return list_control_lots(db)


@router.post("/controls", response_model=ControlLotResponse, status_code=201)
def add_control_lot(body: ControlLotCreate, db: Session = Depends(get_db)):
    """Register a new control lot. Returns 409 if an active duplicate exists."""
    try:
        return create_control_lot(db, body.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
