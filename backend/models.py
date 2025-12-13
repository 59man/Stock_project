from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship 
# -----------------------------
# Lots / Transactions Table
# -----------------------------
class LotDB(Base):
    __tablename__ = "lots"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String, nullable=True)
    bought_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to AssetDB (optional, for ORM queries)
    asset = relationship("AssetDB", back_populates="lots")



# ============================================================
# SQLAlchemy Database Models (Database Tables)
# ============================================================

class AssetDB(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=True, unique=True, index=True)
    isin = Column(String, index=True)
    type = Column(String, nullable=False)
    provider = Column(String, nullable=True)
    currency = Column(String, nullable=True)

    lots = relationship("LotDB", back_populates="asset", cascade="all, delete")

# ============================================================
# Pydantic Models (API Input/Output)
# ============================================================

# User input → creating a new asset
class AssetCreate(BaseModel):
    isin: str
    manual_name: str | None = None
    manual_price: float | None = None



class AssetResponse(BaseModel):
    id: int
    name: str
    symbol: str | None
    isin: str
    type: str
    provider: str | None
    currency: str | None

    class Config:
        orm_mode = True

class LotCreate(BaseModel):
    asset_id: int
    quantity: float
    price: float
    currency: str | None = None
    bought_at: datetime | None = None


class LotResponse(BaseModel):
    id: int
    asset_id: int
    quantity: float
    price: float
    currency: str | None = None
    bought_at: datetime

    class Config:
        orm_mode = True
        
class MarketPriceResponse(BaseModel):
    asset_id: int
    symbol: str
    price: float | None
    currency: str | None
    timestamp: datetime | None