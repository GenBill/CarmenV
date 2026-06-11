from pathlib import Path
from typing import Any

import yaml

from carmenv.agents.consensus import summarize_consensus
from carmenv.agents.schema import CouncilResult, PersonaDefinition, PersonaOpinion, Stance

DEFAULT_PERSONA_DIR = Path(__file__).with_name("personas")


def run_persona_council(
    ticker: str,
    context_pack: dict[str, Any],
    persona_dir: Path | None = None,
) -> CouncilResult:
    """Run a deterministic persona council without calling any LLM.

    Each persona is loaded from YAML and evaluated by its `scoring_rubric` against
    numeric fields in `context_pack`. Missing evidence is treated as neutral (50),
    keeping the interface stable while future LLM/VLM implementations are added.
    """
    personas = load_personas(persona_dir or DEFAULT_PERSONA_DIR)
    opinions = [_evaluate_persona(ticker, persona, context_pack) for persona in personas]
    return CouncilResult(
        ticker=ticker,
        opinions=opinions,
        consensus=summarize_consensus(opinions),
        context_keys=sorted(context_pack.keys()),
    )


def load_personas(persona_dir: Path = DEFAULT_PERSONA_DIR) -> list[PersonaDefinition]:
    persona_paths = sorted(persona_dir.glob("*.yaml"))
    return [
        PersonaDefinition.model_validate(yaml.safe_load(path.read_text())) for path in persona_paths
    ]


def _evaluate_persona(
    ticker: str,
    persona: PersonaDefinition,
    context_pack: dict[str, Any],
) -> PersonaOpinion:
    weighted_score = 0.0
    total_weight = 0.0
    evidence: list[str] = []
    concerns: list[str] = []

    for signal_name, weight in persona.scoring_rubric.items():
        score = _signal_score(signal_name, context_pack)
        weighted_score += score * weight
        total_weight += weight
        source_signal = _source_signal_name(signal_name)
        if score >= 65:
            evidence.append(f"{source_signal} supportive ({score:.1f})")
        elif score <= 40:
            concerns.append(f"{source_signal} weak ({score:.1f})")

    final_score = round(weighted_score / total_weight if total_weight else 50.0, 2)
    stance = _stance_from_score(final_score)
    confidence = _confidence_from_inputs(persona, context_pack, final_score)
    if not evidence:
        evidence.append("No strong positive evidence; neutral defaults used for missing fields.")
    if not concerns:
        concerns.append("No major persona-specific concern in the supplied context pack.")

    return PersonaOpinion(
        ticker=ticker,
        persona_name=persona.name,
        score=final_score,
        stance=stance,
        confidence=confidence,
        evidence=evidence,
        concerns=concerns,
    )


def _signal_score(signal_name: str, context_pack: dict[str, Any]) -> float:
    invert = signal_name.startswith("invert_")
    raw_name = _source_signal_name(signal_name)
    raw_value = context_pack.get(raw_name, 50.0)
    score = _normalize_signal(raw_name, raw_value)
    if invert:
        score = 100.0 - score
    return max(0.0, min(100.0, score))


def _source_signal_name(signal_name: str) -> str:
    return signal_name.removeprefix("invert_")


def _normalize_signal(signal_name: str, raw_value: Any) -> float:
    if raw_value is None:
        return 50.0
    value = float(raw_value)
    if signal_name in {"return_1d", "return_5d", "return_20d"}:
        return 50.0 + max(-0.25, min(0.25, value)) * 200
    if signal_name == "volatility_20d":
        return min(100.0, max(0.0, value * 1000))
    if signal_name == "amount_ma20":
        return min(100.0, max(0.0, value / 1_000_000 * 20))
    if 0 <= value <= 1:
        return value * 100
    return max(0.0, min(100.0, value))


def _stance_from_score(score: float) -> Stance:
    if score >= 65:
        return "bullish"
    if score <= 40:
        return "bearish"
    return "neutral"


def _confidence_from_inputs(
    persona: PersonaDefinition, context_pack: dict[str, Any], score: float
) -> float:
    source_signals = {_source_signal_name(signal) for signal in persona.scoring_rubric}
    coverage = sum(signal in context_pack for signal in source_signals) / len(source_signals)
    conviction = abs(score - 50) / 50
    return round(max(0.15, min(0.95, 0.25 + coverage * 0.45 + conviction * 0.30)), 2)
