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


def filter_10k_10q(filings_data: dict) -> list[dict]:
    """
    Given the raw dict from get_company_filings, return a clean list of
    just the 10-K and 10-Q filings, each as its own dict.
    """
    recent = filings_data["filings"]["recent"]
    results = []

    for i, form_type in enumerate(recent["form"]):
        if form_type in ("10-K", "10-Q"):
            accession = recent["accessionNumber"][i].replace("-", "")
            primary_doc = recent["primaryDocument"][i]
            cik = filings_data["cik"]

            doc_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik}/{accession}/{primary_doc}"
            )

            results.append({
                "form": form_type,
                "filing_date": recent["filingDate"][i],
                "accession_number": recent["accessionNumber"][i],
                "document_url": doc_url,
            })

    return results


if __name__ == "__main__":
    # Quick manual test: pull Apple's filings, filter to 10-K/10-Q, show the latest 3
    data = get_company_filings("0000320193")
    print(data["name"])

    filings = filter_10k_10q(data)
    print(f"Found {len(filings)} 10-K/10-Q filings")
    for f in filings[:3]:
        print(f)
