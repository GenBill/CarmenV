import pandas as pd


def add_score_bucket(scores: pd.DataFrame, bucket_size: int = 20) -> pd.DataFrame:
    out = scores.copy()
    out["score_bucket"] = (out["final_score"] // bucket_size * bucket_size).astype(int).astype(
        str
    ) + "s"
    return out
