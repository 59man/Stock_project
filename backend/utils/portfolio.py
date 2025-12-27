from sqlalchemy.orm import Session
from models import LotDB, AssetDB
from utils.market_price import get_current_market_price

def calculate_portfolio(db: Session) -> dict:
    """
    Calculate the current portfolio value and per-asset metrics.
    """

    lots = db.query(LotDB).all()

    portfolio_assets = {}
    for lot in lots:
        asset = lot.asset
        if asset.id not in portfolio_assets:
            portfolio_assets[asset.id] = {
                "asset_id": asset.id,
                "name": asset.name,
                "symbol": asset.symbol,
                "quantity": 0.0,
                "invested": 0.0,
                "current_price": None,
                "current_value": 0.0,
                "profit_loss": 0.0,
                "currency": asset.currency
            }

        portfolio_assets[asset.id]["quantity"] += lot.quantity
        portfolio_assets[asset.id]["invested"] += lot.quantity * lot.price

    total_invested = 0.0
    total_value = 0.0

    for asset_id, asset_info in portfolio_assets.items():
        asset = db.query(AssetDB).get(asset_id)

        if asset.symbol:  # Stock / ETF
            price_info = get_current_market_price(asset.symbol)
            current_price = price_info["price"] or 0.0
        else:  # Manual fund
            current_price = asset_info["invested"] / asset_info["quantity"] if asset_info["quantity"] else 0.0

        current_value = current_price * asset_info["quantity"]
        profit_loss = current_value - asset_info["invested"]

        asset_info["current_price"] = current_price
        asset_info["current_value"] = current_value
        asset_info["profit_loss"] = profit_loss

        total_invested += asset_info["invested"]
        total_value += current_value

    return {
        "total_invested": total_invested,
        "total_value": total_value,
        "total_profit_loss": total_value - total_invested,
        "assets": list(portfolio_assets.values())
    }
