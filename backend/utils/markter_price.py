import yfinance as yf


def get_current_market_price(symbol: str):
    """
    Fetch live market price from Yahoo Finance.
    """
    ticker = yf.Ticker(symbol)

    try:
        info = ticker.fast_info
    except Exception:
        info = {}

    return {
        "price": info.get("lastPrice"),
        "currency": info.get("currency"),
        "timestamp": info.get("lastTradeDate"),
    }
