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

def extract_mdna_section(full_text: str) -> str:
    """
    Extract the MD&A (Management's Discussion and Analysis) section from
    10-Q filing text. This is 'Item 2' in Part I of a 10-Q — note that
    Part II also has its own unrelated 'Item 2', so we match on the full
    section title, not just the item number, to avoid grabbing the wrong one.

    SEC filings often use a "curly" apostrophe (’) instead of a straight
    one ('), so we normalize both to match reliably.
    """
    normalized = full_text.replace("\u2019", "'")  # curly apostrophe -> straight

    start_marker = "Management's Discussion and Analysis of Financial Condition and Results of Operations"
    end_marker = "Item 3."

    first_occurrence = normalized.find(start_marker)
    start_index = normalized.find(start_marker, first_occurrence + 1)

    if start_index == -1:
        start_index = first_occurrence

    end_index = normalized.find(end_marker, start_index)

    if start_index == -1 or end_index == -1:
        raise ValueError("Could not locate MD&A section boundaries in filing text")

    return normalized[start_index:end_index].strip()

if __name__ == "__main__":
    text = extract_text_from_html("data/raw/aapl_2026-07-31.htm")
    print(f"Full filing: {len(text)} characters")

    mdna = extract_mdna_section(text)
    print(f"MD&A section: {len(mdna)} characters")
    print("First 500 characters of MD&A:")
    print(mdna[:500])
