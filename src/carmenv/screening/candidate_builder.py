import json

import pandas as pd


def build_baseline_candidates(
    features: pd.DataFrame,
    as_of_date: str,
    min_amount_ma20: float = 1_000_000,
    top_n: int = 50,
) -> pd.DataFrame:
    """Build deterministic baseline candidates from trailing feature rows."""
    if features.empty:
        return _empty_candidates()

    df = features.copy()
    df["date"] = pd.to_datetime(df["date"])
    target_date = pd.to_datetime(as_of_date)
    day = df[df["date"] == target_date].copy()
    if day.empty:
        return _empty_candidates()

    mask = (
        (day["close"] > day["ma20"])
        & (day["ma20"] > day["ma60"])
        & (day["amount_ma20"] > min_amount_ma20)
        & (day["return_20d"] > 0)
        & day["volatility_20d"].notna()
    )
    candidates = day[mask].copy()
    if candidates.empty:
        return _empty_candidates()

    candidates["sort_score"] = (
        candidates["return_20d"].rank(pct=True)
        + candidates["amount_ma20"].rank(pct=True)
        - candidates["volatility_20d"].rank(pct=True) * 0.25
    )
    candidates = (
        candidates.sort_values("sort_score", ascending=False).head(top_n).reset_index(drop=True)
    )
    records = []
    for rank, row in enumerate(candidates.to_dict("records"), start=1):
        snapshot = {
            key: value
            for key, value in row.items()
            if key not in {"date", "ticker", "sort_score"} and pd.notna(value)
        }
        records.append(
            {
                "date": target_date.date(),
                "ticker": row["ticker"],
                "source": "baseline_screen_v1",
                "rank": rank,
                "pattern_type": "trend_liquidity_momentum",
                "close": float(row["close"]),
                "reason": "close>ma20, ma20>ma60, positive 20d return, liquid, volatility present",
                "feature_snapshot": json.dumps(snapshot, default=str),
            }
        )
    return pd.DataFrame.from_records(records)


def _empty_candidates() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "date",
            "ticker",
            "source",
            "rank",
            "pattern_type",
            "close",
            "reason",
            "feature_snapshot",
        ]
    )
