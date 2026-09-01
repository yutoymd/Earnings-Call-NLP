"""
Extracts clean plain text from raw SEC filing HTML.

Note: modern SEC filings use "Inline XBRL", which embeds a hidden block of
machine-readable financial tags (dates, units, accounting concepts) inside
the same HTML file as the human-readable text. That hidden block is not
meant to be visible to readers, so we strip it out explicitly.
"""
import re
import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


def extract_text_from_html(html_path: str) -> str:
    """
    Read a raw HTML filing from disk and return clean plain text.
    """
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "lxml")

    # Remove elements that never contain real filing content
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Remove the hidden Inline XBRL metadata block(s) — these carry
    # display:none styling and/or live inside <ix:header> tags.
    # Some tags have attrs=None rather than {}, so we guard against that.
    for tag in soup.find_all(True):
        attrs = tag.attrs or {}
        style = attrs.get("style", "") or ""
        if "display:none" in style.replace(" ", "").lower():
            tag.decompose()

    for tag in soup.find_all(["ix:header", "ix:hidden"]):
        tag.decompose()

    raw_text = soup.get_text(separator=" ")
    clean_text = re.sub(r"\s+", " ", raw_text).strip()

    return clean_text


if __name__ == "__main__":
    text = extract_text_from_html("data/raw/aapl_2026-07-31.htm")

    print(f"Extracted {len(text)} characters")
    print("First 500 characters:")
    print(text[:500])
