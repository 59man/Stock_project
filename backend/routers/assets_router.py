from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import AssetCreate, AssetResponse, AssetDB
from crud.assets import (
    create_asset_db,
    get_asset_by_id,
    list_assets,
    delete_asset
)

from services.isin_lookup import get_stock_info_from_isin

router = APIRouter(prefix="/assets", tags=["Assets"])


# ============================================================
# Create Asset (auto-filled using ISIN lookup)
# ============================================================

@router.post("/", response_model=AssetResponse)
def api_create_asset(asset: AssetCreate, db: Session = Depends(get_db)):

    info = get_stock_info_from_isin(
        isin=asset.isin,
        manual_name=asset.name
    )

    asset_data = asset.dict()
    asset_data["name"] = info["name"]
    asset_data["symbol"] = info["symbol"] or asset.symbol  # user-defined backup
    asset_data["type"] = info["type"]
    asset_data["provider"] = info["provider"] or "Unknown"
    asset_data["currency"] = info["currency"] or "UNKNOWN"

    # Save to DB
    db_asset = create_asset_db(db, AssetDB(**asset_data))
    return db_asset


# ============================================================
# Get Asset by ID
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
# Delete Asset
# ============================================================

@router.delete("/{asset_id}")
def api_delete_asset(asset_id: int, db: Session = Depends(get_db)):
    success = delete_asset(db, asset_id)
    if not success:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"detail": "Asset deleted"}
