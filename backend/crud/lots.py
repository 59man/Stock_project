from sqlalchemy.orm import Session
from models import LotDB, LotCreate

# Create a new lot / transaction
def create_lot(db: Session, lot: LotCreate):
    db_lot = LotDB(
        asset_id=lot.asset_id,
        quantity=lot.quantity,
        price=lot.price,
        currency=lot.currency,
        bought_at=lot.bought_at or None
    )
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot

# Get lot by ID
def get_lot_by_id(db: Session, lot_id: int):
    return db.query(LotDB).filter(LotDB.id == lot_id).first()

# List all lots
def list_lots(db: Session):
    return db.query(LotDB).all()

# Delete lot by ID
def delete_lot(db: Session, lot_id: int):
    lot = db.query(LotDB).filter(LotDB.id == lot_id).first()
    if lot:
        db.delete(lot)
        db.commit()
        return True
    return False
