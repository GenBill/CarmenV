import pandas as pd

from carmenv.backtest.attribution import summarize_by_score_bucket


def render_weekly_review(
    candidates: pd.DataFrame,
    scores: pd.DataFrame,
    forward_returns: pd.DataFrame,
    top_n: int = 10,
) -> str:
    top = (
        scores.sort_values("final_score", ascending=False).head(top_n)
        if not scores.empty
        else scores
    )
    bucket = summarize_by_score_bucket(scores, forward_returns)
    lines = [
        "# CarmenV Weekly Review",
        "",
        f"本周候选数量: {len(candidates)}",
        "",
        "## Top Candidates",
        _markdown_table(top[["date", "ticker", "final_score", "confidence", "summary"]])
        if not top.empty
        else "No scored candidates yet.",
        "",
        "## 按 final_score 分桶表现",
        _markdown_table(bucket) if not bucket.empty else "No forward return attribution yet.",
        "",
        "## 风险提示",
        "- Baseline scores are deterministic; they exclude fundamentals, news, and broker data.",
        "- Forward returns are research labels, not trading recommendations.",
        "",
        "## 下一步建议",
        "- Accumulate more daily candidates and compare signal buckets by market regime.",
        "- Add manual trade reviews before changing scoring weights.",
    ]
    return "\n".join(lines) + "\n"


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "No data."
    columns = list(df.columns)
    rows = [[str(value) for value in row] for row in df.itertuples(index=False, name=None)]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header, separator, *body])
