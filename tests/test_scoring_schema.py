from datetime import date

import pytest
from pydantic import ValidationError

from carmenv.scoring.schema import AgentScore


def test_agent_score_schema_accepts_valid_scores() -> None:
    score = AgentScore(
        date=date(2026, 6, 11),
        ticker="AAA",
        technical_score=80,
        narrative_score=50,
        fundamental_score=50,
        risk_score=70,
        liquidity_score=90,
        final_score=75,
        confidence=0.6,
        summary="ok",
    )
    assert score.final_score == 75


def test_agent_score_schema_rejects_out_of_range_scores() -> None:
    with pytest.raises(ValidationError):
        AgentScore(
            date=date(2026, 6, 11),
            ticker="AAA",
            technical_score=101,
            narrative_score=50,
            fundamental_score=50,
            risk_score=70,
            liquidity_score=90,
            final_score=75,
            confidence=0.6,
            summary="bad",
        )
