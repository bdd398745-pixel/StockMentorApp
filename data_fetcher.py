import yfinance as yf
import pandas as pd

def get_stock_data(symbol):
    """Fetch data from Yahoo Finance for NSE stock"""
    try:
        ticker = yf.Ticker(symbol + ".NS")
        info = ticker.info
        hist = ticker.history(period="5y")

        return {
            "symbol": symbol.upper(),
            "current_price": info.get("currentPrice"),
            "pe_ratio": info.get("trailingPE"),
            "eps": info.get("trailingEps"),
            "roe": info.get("returnOnEquity"),
            "sector": info.get("sector"),
            "de_ratio": info.get("debtToEquity"),
            "price_history": hist["Close"] if not hist.empty else None
        }
    except Exception as e:
        return {"error": str(e)}


def get_multiple_stocks(symbols):
    """Fetch data for multiple symbols from watchlist"""
    data = []
    for sym in symbols:
        stock = get_stock_data(sym)
        if "error" not in stock:
            data.append(stock)
    return pd.DataFrame(data)
