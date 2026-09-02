# Earnings Call / Filing NLP Alpha Signal

A pipeline that pulls SEC filings (10-K/10-Q) via EDGAR's public API,
extracts quantitative signal from the text (sentiment, tone, hedging
language), and tests whether that signal predicts short-term stock price
reaction around the filing date — using proper event-study methodology
(CAPM-adjusted abnormal returns), not just raw price moves.

Built as a learning project to practice the intersection of NLP, event-study
econometrics, and quant backtesting discipline.

## Pipeline

1. src/edgar_client.py — fetches a company's filing history from SEC
   EDGAR and filters it down to 10-K/10-Q filings with dates and document URLs.
2. src/filing_downloader.py — downloads and saves raw filing HTML locally.
3. src/text_extractor.py — strips HTML tags and hidden Inline XBRL
   metadata, then isolates the MD&A section (Item 2) from a filing.
4. src/sentiment_scorer.py — scores text using the Loughran-McDonald
   financial sentiment dictionary (negative, positive, uncertainty,
   litigious, modal, and constraining language).
5. src/price_data.py — fetches historical daily stock prices via yfinance.

## Next

- CAPM-adjusted event study: estimate expected returns from a market
  model, then compute abnormal returns around each filing date.
- Statistical testing of signal vs. abnormal returns.
- Backtest, with honesty checks (decay over time, transaction costs,
  failure modes).

## Setup

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Create a .env file with:
SEC_USER_AGENT="Your Name your.email@example.com"

(SEC EDGAR requires a User-Agent identifying the requester on every API call.)
