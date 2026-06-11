import pandas as pd


def render_daily_report(candidates: pd.DataFrame, scores: pd.DataFrame) -> str:
    return f"# Daily CarmenV Report\n\nCandidates: {len(candidates)}\nScores: {len(scores)}\n"
