import pandas as pd


def compute_technical_features(daily_bars: pd.DataFrame) -> pd.DataFrame:
    """Compute per-ticker trailing technical features without looking ahead."""
    if daily_bars.empty:
        return pd.DataFrame()

    bars = daily_bars.copy()
    bars["date"] = pd.to_datetime(bars["date"])
    bars = bars.sort_values(["ticker", "date"]).reset_index(drop=True)

    frames: list[pd.DataFrame] = []
    for _, group in bars.groupby("ticker", sort=False):
        g = group.copy().sort_values("date")
        close = g["close"].astype(float)
        high = g["high"].astype(float)
        low = g["low"].astype(float)
        prev_close = close.shift(1)

        for window in (5, 10, 20, 60):
            g[f"ma{window}"] = close.rolling(window=window, min_periods=window).mean()
        g["return_1d"] = close.pct_change(1)
        g["return_5d"] = close.pct_change(5)
        g["return_20d"] = close.pct_change(20)
        g["volatility_20d"] = g["return_1d"].rolling(window=20, min_periods=20).std()
        g["amount_ma20"] = g["amount"].astype(float).rolling(window=20, min_periods=20).mean()

        true_range = pd.concat(
            [(high - low), (high - prev_close).abs(), (low - prev_close).abs()], axis=1
        ).max(axis=1)
        g["atr_14"] = true_range.rolling(window=14, min_periods=14).mean()
        frames.append(
            g[
                [
                    "date",
                    "ticker",
                    "close",
                    "ma5",
                    "ma10",
                    "ma20",
                    "ma60",
                    "return_1d",
                    "return_5d",
                    "return_20d",
                    "volatility_20d",
                    "amount_ma20",
                    "atr_14",
                ]
            ]
        )
    result = pd.concat(frames, ignore_index=True)
    result["date"] = result["date"].dt.date
    return result
