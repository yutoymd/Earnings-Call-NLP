"""
Maps stock tickers to SEC CIK numbers using SEC's official ticker file.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
USER_AGENT = os.getenv("SEC_USER_AGENT")


def load_ticker_to_cik_map() -> dict:
    """
    Downloads SEC's official ticker-to-CIK mapping and returns a dict
    like {"AAPL": "0000320193", "MSFT": "0000789019", ...}.

    CIKs are zero-padded to 10 digits, matching what edgar_client expects.
    """
    url = "https://www.sec.gov/files/company_tickers.json"
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # data is a dict of dicts like {"0": {"cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc."}, ...}
    ticker_to_cik = {}
    for entry in data.values():
        ticker = entry["ticker"]
        cik = str(entry["cik_str"]).zfill(10)
        ticker_to_cik[ticker] = cik

    return ticker_to_cik


if __name__ == "__main__":
    mapping = load_ticker_to_cik_map()
    print(f"Loaded {len(mapping)} ticker mappings")

    for ticker in ["AAPL", "MSFT", "JPM", "XOM", "JNJ"]:
        print(f"{ticker}: {mapping.get(ticker, 'NOT FOUND')}")
