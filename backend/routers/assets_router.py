from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud.lots import get_asset_position
from database import get_db
from models import AssetCreate, AssetResponse, AssetDB
from crud.assets import (
    create_asset,
    get_asset_by_id,
    list_assets,
    delete_asset,
    get_asset_by_symbol
)

from utils.isin_lookup import get_stock_info_from_isin
from utils.market_price import get_current_market_price


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



@router.get("/{asset_id}/price")
def api_get_asset_price(asset_id: int, db: Session = Depends(get_db)):

    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if not asset.symbol:
        raise HTTPException(
            status_code=400,
            detail="Asset has no ticker symbol (manual fund)"
        )

    price_info = get_current_market_price(asset.symbol)

    return {
        "asset_id": asset.id,
        "symbol": asset.symbol,
        "price": price_info["price"],
        "currency": price_info["currency"] or asset.currency,
        "timestamp": price_info["timestamp"],
    }

@router.get("/{asset_id}/position")
def api_get_asset_position(asset_id: int, db: Session = Depends(get_db)):

    asset = get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    quantity = get_asset_position(db, asset_id)

    return {
        "asset_id": asset.id,
        "symbol": asset.symbol,
        "quantity": quantity,
        "currency": asset.currency,
    }