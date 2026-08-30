"""
Client for pulling filing data from SEC EDGAR's public API.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads variables from .env into the environment

USER_AGENT = os.getenv("SEC_USER_AGENT")


def get_company_filings(cik: str) -> dict:
    """
    Fetch a company's filing history from SEC EDGAR.

    cik: the company's SEC 'Central Index Key', zero-padded to 10 digits.
         e.g. Apple's CIK is 320193, so pass "0000320193".
    """
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # throws an error if the request failed

    return response.json()


if __name__ == "__main__":
    # Quick manual test: pull Apple's filings and print the company name
    data = get_company_filings("0000320193")
    print(data["name"])
    print("Most recent filing form:", data["filings"]["recent"]["form"][0])
