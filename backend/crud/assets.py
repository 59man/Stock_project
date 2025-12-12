from sqlalchemy.orm import Session
from models import AssetDB, AssetCreate

# ============================================================
# Create a new asset
# ============================================================

def create_asset(db: Session, asset: AssetCreate) -> AssetDB:
    db_asset = AssetDB(
        name=asset.name,
        symbol=asset.symbol,
        isin=asset.isin,
        type=asset.type,
        provider=asset.provider,
        currency=asset.currency
    )
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset


# ============================================================
# Get asset by ID
# ============================================================

def get_asset_by_id(db: Session, asset_id: int) -> AssetDB | None:
    return db.query(AssetDB).filter(AssetDB.id == asset_id).first()


# ============================================================
# Get asset by symbol
# ============================================================

def get_asset_by_symbol(db: Session, symbol: str) -> AssetDB | None:
    return db.query(AssetDB).filter(AssetDB.symbol == symbol).first()


# ============================================================
# Get asset by ISIN
# ============================================================

def get_asset_by_isin(db: Session, isin: str) -> AssetDB | None:
    return db.query(AssetDB).filter(AssetDB.isin == isin).first()


# ============================================================
# List all assets
# ============================================================

def list_assets(db: Session) -> list[AssetDB]:
    return db.query(AssetDB).all()


# ============================================================
# Delete asset
# ============================================================

def delete_asset(db: Session, asset_id: int) -> bool:
    asset = get_asset_by_id(db, asset_id)
    if not asset:
        return False

    db.delete(asset)
    db.commit()
    return True
