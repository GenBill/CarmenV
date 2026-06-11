import pandas as pd


def summarize_by_score_bucket(scores: pd.DataFrame, forward_returns: pd.DataFrame) -> pd.DataFrame:
    if scores.empty or forward_returns.empty:
        return _empty_summary(["score_bucket", "horizon_days"])
    merged = forward_returns.merge(scores[["date", "ticker", "final_score"]], on=["date", "ticker"])
    merged["score_bucket"] = pd.cut(
        merged["final_score"], bins=[0, 20, 40, 60, 80, 100], include_lowest=True
    ).astype(str)
    return _summarize(merged, ["score_bucket", "horizon_days"])


def summarize_by_pattern_type(
    candidates: pd.DataFrame, forward_returns: pd.DataFrame
) -> pd.DataFrame:
    if candidates.empty or forward_returns.empty:
        return _empty_summary(["pattern_type", "horizon_days"])
    merged = forward_returns.merge(
        candidates[["date", "ticker", "pattern_type"]], on=["date", "ticker"]
    )
    return _summarize(merged, ["pattern_type", "horizon_days"])


def summarize_by_horizon(forward_returns: pd.DataFrame) -> pd.DataFrame:
    if forward_returns.empty:
        return _empty_summary(["horizon_days"])
    return _summarize(forward_returns, ["horizon_days"])


def _summarize(df: pd.DataFrame, by: list[str]) -> pd.DataFrame:
    grouped = df.groupby(by, dropna=False)
    return grouped.agg(
        count=("return_pct", "count"),
        mean_return=("return_pct", "mean"),
        median_return=("return_pct", "median"),
        win_rate=("return_pct", lambda s: (s > 0).mean()),
        mean_max_drawdown=("max_drawdown_pct", "mean"),
    ).reset_index()


def _empty_summary(columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        columns=columns + ["count", "mean_return", "median_return", "win_rate", "mean_max_drawdown"]
    )
