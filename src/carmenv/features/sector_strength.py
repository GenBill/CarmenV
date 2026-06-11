import pandas as pd


def compute_sector_strength(features: pd.DataFrame, symbol_sector: pd.DataFrame) -> pd.DataFrame:
    if features.empty or symbol_sector.empty:
        return pd.DataFrame(columns=["date", "sector", "mean_return_20d"])
    merged = features.merge(symbol_sector[["ticker", "sector"]], on="ticker", how="left")
    return (
        merged.groupby(["date", "sector"], as_index=False)["return_20d"]
        .mean()
        .rename(columns={"return_20d": "mean_return_20d"})
    )
