from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from crud.portfolio import get_portfolio

from utils.portfolio import calculate_portfolio 

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


@router.get("/")
def api_get_portfolio(db: Session = Depends(get_db)):
    return get_portfolio(db)