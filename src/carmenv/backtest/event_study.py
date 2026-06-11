import pandas as pd


def average_return_by_horizon(forward_returns: pd.DataFrame) -> pd.DataFrame:
    if forward_returns.empty:
        return pd.DataFrame(columns=["horizon_days", "mean_return"])
    return (
        forward_returns.groupby("horizon_days", as_index=False)["return_pct"]
        .mean()
        .rename(columns={"return_pct": "mean_return"})
    )
