from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import AssetCreate, AssetResponse
from crud.assets import (
    create_asset,
    get_asset_by_id,
    get_asset_by_symbol,
    list_assets,
    delete_asset
)

router = APIRouter(prefix="/assets", tags=["Assets"])


# ============================================================
# Create a new asset
# ============================================================

@router.post("/", response_model=AssetResponse)
def api_create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    # Prevent duplicate ticker symbols
    existing = get_asset_by_symbol(db, asset.symbol)
    if existing:
        raise HTTPException(status_code=400, detail="Asset with this symbol already exists")

    new_asset = create_asset(db, asset)
    return new_asset


# ============================================================
# Get asset by ID
# ============================================================

@router.get("/{asset_id}", response_model=AssetResponse)
def api_get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


# ============================================================
# List all assets
# ============================================================

@router.get("/", response_model=list[AssetResponse])
def api_list_assets(db: Session = Depends(get_db)):
    return list_assets(db)


# ============================================================
# Delete asset
# ============================================================

@router.delete("/{asset_id}")
def api_delete_asset(asset_id: int, db: Session = Depends(get_db)):
    success = delete_asset(db, asset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"detail": "Asset deleted"}
