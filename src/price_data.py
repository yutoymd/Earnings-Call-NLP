"""
Fetches historical stock price data for event-study analysis.
"""
import yfinance as yf
import pandas as pd


def get_price_history(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch daily historical price data for a ticker between two dates.

    ticker: e.g. "AAPL"
    start_date, end_date: "YYYY-MM-DD" strings

    Returns a DataFrame indexed by date with plain columns (Open, High,
    Low, Close, Volume) — yfinance returns a MultiIndex (Price, Ticker)
    even for a single ticker, so we flatten it here to keep downstream
    code simple.
    """
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        raise ValueError(f"No price data returned for {ticker} between {start_date} and {end_date}")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data

if __name__ == "__main__":
    # Quick manual test: pull ~2 weeks of Apple prices around the filing
    # date we've been working with (2026-07-31)
    prices = get_price_history("AAPL", "2026-07-20", "2026-08-10")

    print(f"Fetched {len(prices)} trading days")
    print(prices[["Close"]].head(10))
