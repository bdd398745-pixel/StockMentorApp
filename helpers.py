import pandas as pd

def format_number(num):
    if num is None:
        return "-"
    if num >= 1e7:
        return f"{num/1e7:.2f} Cr"
    elif num >= 1e5:
        return f"{num/1e5:.2f} L"
    return f"{num:.2f}"

def load_watchlist():
    try:
        df = pd.read_csv("watchlist.csv")
        return df
    except:
        return pd.DataFrame(columns=["symbol", "company"])
