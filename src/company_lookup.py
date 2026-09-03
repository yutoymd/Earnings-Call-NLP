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

def load_company_list(txt_path: str, ticker_to_cik: dict) -> list[dict]:
    """
    Read a plain-text file of tickers (one per line) and resolve each to
    its CIK using the provided ticker_to_cik mapping.

    Returns a list of dicts like [{"ticker": "AAPL", "cik": "0000320193"}, ...].
    Raises an error listing any tickers that couldn't be resolved, so bad
    entries (typos, delistings, recent renames) are caught early rather
    than failing partway through a long pipeline run later.
    """
    with open(txt_path, "r") as f:
        tickers = [line.strip().upper() for line in f if line.strip()]

    resolved = []
    missing = []

    for ticker in tickers:
        cik = ticker_to_cik.get(ticker)
        if cik is None:
            missing.append(ticker)
        else:
            resolved.append({"ticker": ticker, "cik": cik})

    if missing:
        raise ValueError(f"Could not resolve CIK for tickers: {missing}")

    return resolved

if __name__ == "__main__":
    mapping = load_ticker_to_cik_map()
    print(f"Loaded {len(mapping)} ticker mappings")

    companies = load_company_list("config/companies.txt", mapping)
    print(f"\nResolved {len(companies)} companies:")
    for c in companies:
        print(f"  {c['ticker']}: {c['cik']}")
