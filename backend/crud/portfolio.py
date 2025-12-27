from sqlalchemy.orm import Session
from sqlalchemy import func
from utils.market_price import get_current_market_price

from models import AssetDB, LotDB


def get_holdings(db: Session):
    """
    Aggregate lots into holdings per asset
    """

    rows = (
        db.query(
            AssetDB.id.label("asset_id"),
            AssetDB.name,
            AssetDB.symbol,
            AssetDB.currency,
            func.sum(LotDB.quantity).label("quantity"),
            func.sum(LotDB.quantity * LotDB.price).label("invested"),
        )
        .join(LotDB, LotDB.asset_id == AssetDB.id)
        .group_by(AssetDB.id)
        .all()
    )

    holdings = []

    for row in rows:
        avg_price = (
            row.invested / row.quantity if row.quantity else 0
        )

        holdings.append({
            "asset_id": row.asset_id,
            "name": row.name,
            "symbol": row.symbol,
            "currency": row.currency,
            "quantity": float(row.quantity),
            "avg_price": float(avg_price),
            "invested": float(row.invested),
        })

    return holdings

def get_portfolio(db: Session):
    holdings = get_holdings(db)

    portfolio = []
    total_value = 0
    total_invested = 0

    for h in holdings:
        if not h["symbol"]:
            continue  # manual funds (handled later)

        price_info = get_current_market_price(h["symbol"])
        current_price = price_info["price"] or 0

        current_value = current_price * h["quantity"]
        pnl = current_value - h["invested"]
        pnl_pct = (pnl / h["invested"] * 100) if h["invested"] else 0

        total_value += current_value
        total_invested += h["invested"]

        portfolio.append({
            **h,
            "current_price": current_price,
            "current_value": current_value,
            "pnl": pnl,
            "pnl_pct": pnl_pct,
        })

    return {
        "assets": portfolio,
        "total_invested": total_invested,
        "total_value": total_value,
        "total_pnl": total_value - total_invested,
        "total_pnl_pct": (
            (total_value - total_invested) / total_invested * 100
            if total_invested else 0
        ),
    }