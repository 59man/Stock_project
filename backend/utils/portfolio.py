from sqlalchemy.orm import Session
from models import LotDB
from utils.market_price import get_current_market_price


def calculate_portfolio(db: Session) -> dict:
    """
    Calculate portfolio totals and per-asset metrics including
    current price, market value, and P/L.
    """

    lots = db.query(LotDB).all()

    portfolio_assets: dict[int, dict] = {}

    # ------------------------------------------------------------
    # Aggregate lots per asset
    # ------------------------------------------------------------
    for lot in lots:
        asset = lot.asset

        if asset.id not in portfolio_assets:
            portfolio_assets[asset.id] = {
                "asset_id": asset.id,
                "name": asset.name,
                "symbol": asset.symbol,
                "currency": asset.currency,
                "quantity": 0.0,
                "invested": 0.0,
                "average_price": 0.0,
                "current_price": None,
                "current_value": 0.0,
                "profit_loss": 0.0,
                "profit_loss_pct": None,
            }

        portfolio_assets[asset.id]["quantity"] += lot.quantity
        portfolio_assets[asset.id]["invested"] += lot.quantity * lot.price

    total_invested = 0.0
    total_value = 0.0

    # ------------------------------------------------------------
    # Calculate metrics per asset
    # ------------------------------------------------------------
    for asset_info in portfolio_assets.values():
        qty = asset_info["quantity"]
        invested = asset_info["invested"]

        asset_info["average_price"] = invested / qty if qty else 0.0

        # --- Get market price ---
        if asset_info["symbol"]:
            price_info = get_current_market_price(asset_info["symbol"])
            current_price = (
                price_info.get("price")
                if isinstance(price_info, dict)
                else None
            )
        else:
            # Manual / custom asset fallback
            current_price = asset_info["average_price"]

        current_price = current_price or 0.0
        current_value = current_price * qty
        profit_loss = current_value - invested

        asset_info["current_price"] = current_price
        asset_info["current_value"] = current_value
        asset_info["profit_loss"] = profit_loss
        asset_info["profit_loss_pct"] = (
            (profit_loss / invested) * 100 if invested else None
        )

        total_invested += invested
        total_value += current_value

    # ------------------------------------------------------------
    # Portfolio totals
    # ------------------------------------------------------------
    return {
        "total_invested": total_invested,
        "total_value": total_value,
        "total_profit_loss": total_value - total_invested,
        "total_profit_loss_pct": (
            ((total_value - total_invested) / total_invested) * 100
            if total_invested
            else None
        ),
        "assets": list(portfolio_assets.values()),
    }
