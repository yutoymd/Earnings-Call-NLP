"""
Event-study methodology: computes CAPM-adjusted abnormal returns around
a corporate event (e.g. a filing date).
"""
import numpy as np
import pandas as pd


def compute_daily_returns(prices: pd.DataFrame, price_col: str = "Close") -> pd.Series:
    """
    Convert a price series into daily percentage returns.
    return_t = (price_t / price_t-1) - 1
    """
    return prices[price_col].pct_change().dropna()


def estimate_market_model(stock_returns: pd.Series, market_returns: pd.Series) -> tuple[float, float]:
    """
    Estimate CAPM alpha and beta via simple linear regression:
        stock_return = alpha + beta * market_return

    Both series must be aligned on the same dates. Returns (alpha, beta).
    """
    aligned = pd.concat([stock_returns, market_returns], axis=1, join="inner")
    aligned.columns = ["stock", "market"]

    # np.polyfit fits a line: degree 1 = slope (beta) and intercept (alpha)
    beta, alpha = np.polyfit(aligned["market"], aligned["stock"], deg=1)

    return alpha, beta


def compute_abnormal_returns(
    stock_returns: pd.Series,
    market_returns: pd.Series,
    alpha: float,
    beta: float,
) -> pd.Series:
    """
    Given actual stock/market returns and an estimated market model,
    compute abnormal returns: actual - expected, for each date.
    """
    aligned = pd.concat([stock_returns, market_returns], axis=1, join="inner")
    aligned.columns = ["stock", "market"]

    expected_return = alpha + beta * aligned["market"]
    abnormal_return = aligned["stock"] - expected_return

    return abnormal_return


if __name__ == "__main__":
    from price_data import get_price_history

    # Estimation window: a clean period well before the filing date,
    # used to learn the stock's "normal" relationship to the market
    est_stock = get_price_history("AAPL", "2026-01-01", "2026-06-30")
    est_market = get_price_history("^GSPC", "2026-01-01", "2026-06-30")

    stock_est_returns = compute_daily_returns(est_stock)
    market_est_returns = compute_daily_returns(est_market)

    alpha, beta = estimate_market_model(stock_est_returns, market_est_returns)
    print(f"Estimated alpha: {alpha:.6f}")
    print(f"Estimated beta: {beta:.4f}")

    # Event window: around the actual filing date (2026-07-31)
    event_stock = get_price_history("AAPL", "2026-07-28", "2026-08-04")
    event_market = get_price_history("^GSPC", "2026-07-28", "2026-08-04")

    stock_event_returns = compute_daily_returns(event_stock)
    market_event_returns = compute_daily_returns(event_market)

    abnormal = compute_abnormal_returns(stock_event_returns, market_event_returns, alpha, beta)
    print("\nAbnormal returns around filing date:")
    print(abnormal)

    print(f"\nCumulative abnormal return (CAR): {abnormal.sum():.4%}")
