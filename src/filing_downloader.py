"""
Downloads raw filing documents from SEC EDGAR and saves them locally.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
USER_AGENT = os.getenv("SEC_USER_AGENT")


def download_filing(document_url: str, save_path: str) -> str:
    """
    Download the raw HTML of a filing and save it to disk.

    document_url: the direct URL to the filing document (from filter_10k_10q)
    save_path: where to save the raw HTML file, e.g. 'data/raw/aapl_2026-07-31.htm'

    Returns the save_path for convenience.
    """
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(document_url, headers=headers)
    response.raise_for_status()

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return save_path


if __name__ == "__main__":
    # Quick manual test: download the most recent Apple 10-Q we found earlier
    test_url = "https://www.sec.gov/Archives/edgar/data/0000320193/000032019326000020/aapl-20260627.htm"
    path = download_filing(test_url, "data/raw/aapl_2026-07-31.htm")
    print(f"Saved to {path}")

    # Confirm it actually saved something real
    size_kb = os.path.getsize(path) / 1024
    print(f"File size: {size_kb:.1f} KB")
