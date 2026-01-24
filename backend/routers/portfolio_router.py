from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session

from database import get_db
from crud.portfolio import get_portfolio,get_asset_portfolio

from utils.portfolio import calculate_portfolio 

from models import AssetPortfolioResponse

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/")
def api_get_portfolio(db: Session = Depends(get_db)):
    return calculate_portfolio(db)


@router.get("/asset/{asset_id}", response_model=AssetPortfolioResponse)
def api_get_asset_portfolio(asset_id: int, db: Session = Depends(get_db)):
    data = get_asset_portfolio(db, asset_id)

    if data["total_quantity"] == 0:
        raise HTTPException(status_code=404, detail="No lots for this asset")

    return data