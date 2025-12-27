import yfinance as yf
from datetime import datetime


def get_current_market_price(symbol: str):
    ticker = yf.Ticker(symbol)

    try:
        data = ticker.fast_info
        price = data.get("lastPrice")
        currency = data.get("currency")
    except Exception:
        price = None
        currency = None

    return {
        "price": price,
        "currency": currency,
        "timestamp": datetime.utcnow(),
    }
