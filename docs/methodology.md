# Methodology

## Why not just look at raw price moves?

[Explain in your own words: what's wrong with saying "the stock dropped
2% after the filing, so the filing was bad news"? Think about what else
could cause a stock to move on any given day.]

## The CAPM market model

The core idea: a stock's "normal" expected return on any given day can
be estimated from how the overall market moved that day, using two
parameters:

    expected_return = alpha + beta * market_return

- alpha: the stock's average return independent of the market
- beta: how sensitive the stock is to market-wide moves (beta > 1 means
  more volatile than the market, beta < 1 means less)

## Event-study steps

1. **Estimation window**: a clean period before the event (we use
   ~6 months ending well before the filing date) is used to estimate
   alpha and beta via linear regression of stock returns on market
   returns.

2. **Event window**: a short period around the actual filing date
   (we use 1 day before to 1 day after). The estimated alpha/beta from
   step 1 are used to calculate what the stock's return *should* have
   been each day, given the actual market return that day.

3. **Abnormal return (AR)**: actual return - expected return, for each
   day in the event window.

4. **Cumulative abnormal return (CAR)**: the sum of abnormal returns
   across the event window. This is the metric we'll test against our
   NLP sentiment signal — it represents the part of the stock's move
   that market-wide conditions don't explain.

## Why this matters for the NLP signal

[Explain in your own words: why is CAR a better thing to correlate with
sentiment scores than the raw stock return would be?]

## Example result (AAPL, 2026-07-31 10-Q)

- Estimated beta: 0.83
- Cumulative abnormal return: -12.98%
- This suggests Apple's stock move around this filing was substantially
  larger than general market conditions would explain — something
  specific to this filing likely drove the reaction.
