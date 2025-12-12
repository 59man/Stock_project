from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import LotCreate, LotResponse
from crud.lots import create_lot, get_lot_by_id, list_lots, delete_lot
from crud.assets import get_asset_by_id

router = APIRouter(prefix="/lots", tags=["Lots"])


# ============================================================
# Create Lot (manual price allowed)
# ============================================================

@router.post("/", response_model=LotResponse)
def api_create_lot(lot: LotCreate, db: Session = Depends(get_db)):

    # ✔️ ensure the asset exists
    asset = get_asset_by_id(db, lot.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset does not exist")

    # ✔️ create the transaction with the manual price
    return create_lot(db, lot)


# ============================================================
# List Lots
# ============================================================

@router.get("/", response_model=list[LotResponse])
def api_list_lots(db: Session = Depends(get_db)):
    return list_lots(db)


# ============================================================
# Get Lot by ID
# ============================================================

@router.get("/{lot_id}", response_model=LotResponse)
def api_get_lot(lot_id: int, db: Session = Depends(get_db)):
    lot = get_lot_by_id(db, lot_id)
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")
    return lot


# ============================================================
# Delete Lot
# ============================================================

@router.delete("/{lot_id}")
def api_delete_lot(lot_id: int, db: Session = Depends(get_db)):
    success = delete_lot(db, lot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lot not found")
    return {"detail": "Lot deleted"}
