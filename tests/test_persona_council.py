from carmenv.agents.consensus import disagreement_score, summarize_consensus
from carmenv.agents.council import load_personas, run_persona_council
from carmenv.agents.schema import PersonaOpinion


def test_persona_yaml_definitions_have_required_fields() -> None:
    personas = load_personas()

    assert {persona.name for persona in personas} == {
        "serenity_chokepoint",
        "value_investor",
        "technical_trader",
        "industry_researcher",
        "quant_factor",
        "risk_manager",
        "short_seller",
    }
    for persona in personas:
        assert persona.philosophy
        assert persona.preferred_evidence
        assert persona.blind_spots
        assert persona.scoring_rubric
        assert persona.output_schema["stance"] == "bullish_neutral_bearish"


def test_run_persona_council_returns_structured_mock_result() -> None:
    result = run_persona_council(
        "AAA",
        {
            "technical_score": 82,
            "narrative_score": 88,
            "fundamental_score": 61,
            "risk_score": 72,
            "liquidity_score": 77,
            "industry_score": 90,
            "moat_score": 84,
            "momentum_score": 80,
            "quality_score": 64,
            "valuation_score": 58,
            "drawdown_risk_score": 70,
            "thesis_risk_score": 35,
            "volatility_20d": 0.018,
        },
    )

    assert result.ticker == "AAA"
    assert len(result.opinions) == 7
    assert result.consensus.mean_score > 60
    assert result.consensus.bullish_count >= 3
    assert result.consensus.disagreement_score >= 0
    assert "technical_score" in result.context_keys
    assert result.model_dump()["consensus"]["consensus_score"] >= 0


def test_consensus_disagreement_increases_with_stance_conflict() -> None:
    aligned = [
        PersonaOpinion(ticker="AAA", persona_name="p1", score=70, stance="bullish", confidence=0.7),
        PersonaOpinion(ticker="AAA", persona_name="p2", score=72, stance="bullish", confidence=0.7),
    ]
    conflicted = [
        PersonaOpinion(ticker="AAA", persona_name="p1", score=85, stance="bullish", confidence=0.7),
        PersonaOpinion(ticker="AAA", persona_name="p2", score=50, stance="neutral", confidence=0.7),
        PersonaOpinion(ticker="AAA", persona_name="p3", score=25, stance="bearish", confidence=0.7),
    ]

    assert disagreement_score(conflicted) > disagreement_score(aligned)
    summary = summarize_consensus(conflicted)
    assert summary.bullish_count == 1
    assert summary.neutral_count == 1
    assert summary.bearish_count == 1
