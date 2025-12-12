from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base
# ============================================================
# SQLAlchemy Database Models (Database Tables)
# ============================================================

class AssetDB(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False, unique=True, index=True)
    isin = Column(String, index=True)
    type = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    currency = Column(String, nullable=False)

# ============================================================
# Pydantic Models (API Input/Output)
# ============================================================

# User input → creating a new asset
class AssetCreate(BaseModel):
    name: str
    symbol: str
    isin: str | None = None
    type: str
    provider: str
    currency: str



# Output returned by the API when sending asset info
class AssetResponse(BaseModel):
    id: int
    name: str
    symbol: str
    isin: str | None = None
    type: str
    provider: str
    currency: str

    class Config:
        orm_mode = True

