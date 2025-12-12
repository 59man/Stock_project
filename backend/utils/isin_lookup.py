import yfinance as yf

# Optional: a local mapping of ISIN → ticker
ISIN_TO_TICKER = {
    "US0378331005": "AAPL",   # Apple
    "US5949181045": "MSFT",   # Microsoft
    "CZ0009008942": "CZG",        # Colt CZ Group SE
    "CS0008418869": "TABAK",      # Philip Morris ČR
    "AT0000908504": "VIG",        # Vienna Insurance Group AG
    "CZ0008040318": "MONET",      # Moneta Money Bank
    "DE000A0S9GB0": "4GLD",        # Xetra‑Gold ETC
    # Mutual fund share classes (no universal ticker):
    "CZ0008475720": None,         # Fio Globální akciový fond (CZK)
    "LU2595011649": None,         # Pictet Global Opportunities Allocation Fund (example)
    "LU1756523376": None,         # Fidelity World Fund (CZK)
    "LU26006422355":None,           #onemarkets blakrokck global equity fund
}


def get_stock_info_from_isin(isin: str, manual_name: str | None = None):
    """
    Look up market info from ISIN → ticker → yfinance.
    Price is intentionally NOT included because only lots store price.
    """
    ticker_symbol = ISIN_TO_TICKER.get(isin)

    # Case 1: Normal stock / ETF with defined ticker
    if ticker_symbol:
        yf_ticker = yf.Ticker(ticker_symbol)

        try:
            info = yf_ticker.info
        except Exception:
            info = {}

        return {
            "name": info.get("longName") or info.get("shortName") or ticker_symbol,
            "symbol": ticker_symbol,
            "type": info.get("quoteType") or "Equity",
            "provider": info.get("exchange") or "UNKNOWN",
            "currency": info.get("currency") or "USD",
        }

    # Case 2: No ticker (fund) → use manual data
    return {
        "name": manual_name or "Unknown Fund",
        "symbol": None,
        "type": "Fund",
        "provider": "manual",
        "currency": None,  # user must enter manually
    }

