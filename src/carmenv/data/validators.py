import pandas as pd

REQUIRED_DAILY_BAR_COLUMNS = {"date", "ticker", "open", "high", "low", "close", "volume", "amount"}


def validate_daily_bars(df: pd.DataFrame) -> None:
    missing = REQUIRED_DAILY_BAR_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"daily bars missing columns: {sorted(missing)}")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError("OHLC prices must be positive")
