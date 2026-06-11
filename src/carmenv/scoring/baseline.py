import json
from typing import Any

import pandas as pd

from carmenv.scoring.schema import AgentScore


def score_candidate(
    candidate: dict[str, Any] | pd.Series, features: dict[str, Any] | pd.Series | None = None
) -> AgentScore:
    """Score one candidate with deterministic non-LLM rules."""
    cand = candidate.to_dict() if isinstance(candidate, pd.Series) else dict(candidate)
    snapshot: dict[str, Any] = {}
    if features is not None:
        snapshot = features.to_dict() if isinstance(features, pd.Series) else dict(features)
    elif cand.get("feature_snapshot"):
        raw = cand["feature_snapshot"]
        snapshot = json.loads(raw) if isinstance(raw, str) else dict(raw)

    close = float(snapshot.get("close", cand.get("close", 0)) or 0)
    ma20 = float(snapshot.get("ma20", close) or close)
    ma60 = float(snapshot.get("ma60", ma20) or ma20)
    ret20 = float(snapshot.get("return_20d", 0) or 0)
    vol20 = float(snapshot.get("volatility_20d", 0) or 0)
    amount_ma20 = float(snapshot.get("amount_ma20", 0) or 0)

    trend_score = _clamp(50 + min(max(ret20, -0.2), 0.2) * 150 + (close / ma20 - 1) * 100)
    liquidity_score = _clamp(40 + min(amount_ma20 / 1_000_000, 40))
    risk_score = _clamp(85 - min(vol20 * 500, 60) + (10 if ma20 > ma60 else -20))
    narrative_score = 50.0
    fundamental_score = 50.0
    final_score = _clamp(
        trend_score * 0.38
        + liquidity_score * 0.18
        + risk_score * 0.22
        + narrative_score * 0.11
        + fundamental_score * 0.11
    )
    return AgentScore(
        date=cand["date"],
        ticker=cand["ticker"],
        technical_score=round(trend_score, 2),
        narrative_score=narrative_score,
        fundamental_score=fundamental_score,
        risk_score=round(risk_score, 2),
        liquidity_score=round(liquidity_score, 2),
        final_score=round(final_score, 2),
        confidence=0.55,
        summary="Deterministic baseline score from trend, liquidity, and volatility features.",
    )


def score_candidates(candidates: pd.DataFrame) -> pd.DataFrame:
    if candidates.empty:
        return pd.DataFrame(columns=list(AgentScore.model_fields))
    return pd.DataFrame([score_candidate(row).model_dump() for _, row in candidates.iterrows()])


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, float(value)))
