from datetime import date

import pandas as pd
from pydantic import BaseModel, Field


class ForwardReturn(BaseModel):
    date: date
    ticker: str
    horizon_days: int = Field(gt=0)
    entry_close: float
    future_close: float | None = None
    return_pct: float | None = None
    max_drawdown_pct: float | None = None
    max_runup_pct: float | None = None
    hit_stop_loss: bool | None = None


def compute_forward_returns(
    candidates: pd.DataFrame,
    daily_bars: pd.DataFrame,
    horizons: list[int],
) -> pd.DataFrame:
    """Compute forward returns from each candidate date close.

    The entry price is the candidate day's close. Horizon N means the close N future
    trading rows after the candidate row for the same ticker. If a ticker lacks enough
    future rows for a requested horizon, that candidate/horizon row is skipped rather
    than filled with partial future data.
    """
    if candidates.empty or daily_bars.empty:
        return pd.DataFrame(
            columns=[
                "date",
                "ticker",
                "horizon_days",
                "entry_close",
                "future_close",
                "return_pct",
                "max_drawdown_pct",
                "max_runup_pct",
                "hit_stop_loss",
            ]
        )

    bars = daily_bars.copy()
    bars["date"] = pd.to_datetime(bars["date"])
    bars = bars.sort_values(["ticker", "date"]).reset_index(drop=True)
    cand = candidates.copy()
    cand["date"] = pd.to_datetime(cand["date"])

    records: list[dict[str, object]] = []
    for row in cand.itertuples(index=False):
        ticker_bars = bars[bars["ticker"] == row.ticker].reset_index(drop=True)
        matches = ticker_bars.index[ticker_bars["date"] == row.date].tolist()
        if not matches:
            continue
        idx = matches[0]
        entry_close = float(ticker_bars.loc[idx, "close"])
        for horizon in horizons:
            future_idx = idx + horizon
            if future_idx >= len(ticker_bars):
                continue
            window = ticker_bars.loc[idx + 1 : future_idx]
            future_close = float(ticker_bars.loc[future_idx, "close"])
            lows = window["low"].astype(float)
            highs = window["high"].astype(float)
            records.append(
                {
                    "date": row.date.date(),
                    "ticker": row.ticker,
                    "horizon_days": horizon,
                    "entry_close": entry_close,
                    "future_close": future_close,
                    "return_pct": future_close / entry_close - 1,
                    "max_drawdown_pct": lows.min() / entry_close - 1,
                    "max_runup_pct": highs.max() / entry_close - 1,
                    "hit_stop_loss": None,
                }
            )
    return pd.DataFrame.from_records(records)
