import pandas as pd


def classify_market_regime(index_features: pd.DataFrame) -> str:
    if index_features.empty:
        return "unknown"
    latest = index_features.sort_values("date").iloc[-1]
    if latest.get("close", 0) > latest.get("ma20", float("inf")):
        return "risk_on"
    return "neutral_or_risk_off"
