import streamlit as st
import pandas as pd
from data_fetcher import get_stock_data, get_multiple_stocks
from analyzer import fair_value_calc, buy_sell_levels, undervaluation_score
from helpers import load_watchlist, format_number

st.set_page_config(page_title="Stock Mentor", layout="wide")
st.title("📈 StockMentor – Long-Term Stock Advisor (India)")

tab1, tab2 = st.tabs(["🔍 Single Stock", "📊 Watchlist Overview"])

# ------------------- TAB 1 : Single Stock -------------------
with tab1:
    symbol = st.text_input("Enter NSE Stock Symbol (e.g., INFY, ITC, TCS):")

    if symbol:
        data = get_stock_data(symbol)
        if "error" in data:
            st.error(f"Unable to fetch data: {data['error']}")
        else:
            eps = data["eps"]
            fv = fair_value_calc(eps)
            buy, sell = buy_sell_levels(fv)
            score = undervaluation_score(data["current_price"], fv)

            c1, c2, c3 = st.columns(3)
            c1.metric("Current Price", f"₹{data['current_price']}")
            c2.metric("Fair Value", f"₹{fv}")
            c3.metric("Undervaluation", f"{score}%" if score else "-")

            st.write("---")
            st.write(f"**Sector:** {data['sector']}")
            st.write(f"**P/E Ratio:** {data['pe_ratio']}")
            st.write(f"**ROE:** {data['roe']}")
            st.write(f"**Debt/Equity:** {data['de_ratio']}")

            if data["price_history"] is not None:
                st.line_chart(data["price_history"], use_container_width=True)
            else:
                st.warning("No price history found.")

# ------------------- TAB 2 : Watchlist Overview -------------------
with tab2:
    st.subheader("📋 Your Watchlist")

    watchlist = load_watchlist()
    if watchlist.empty:
        st.warning("Watchlist is empty. Add entries to watchlist.csv")
    else:
        df = get_multiple_stocks(watchlist["symbol"].tolist())

        df["fair_value"] = df["eps"].apply(fair_value_calc)
        df["buy_price"], df["sell_price"] = zip(*df["fair_value"].apply(buy_sell_levels))
        df["undervaluation_%"] = df.apply(
            lambda x: undervaluation_score(x["current_price"], x["fair_value"]), axis=1
        )

        df = df.sort_values(by="undervaluation_%", ascending=False)
        st.dataframe(df[["symbol", "current_price", "fair_value", "undervaluation_%", "pe_ratio", "roe", "de_ratio"]])

        best_pick = df.iloc[0]
        st.success(f"🏆 Best undervalued stock currently: **{best_pick['symbol']}** with {best_pick['undervaluation_%']}% undervaluation.")
