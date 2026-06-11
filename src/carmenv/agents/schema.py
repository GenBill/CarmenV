from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

Stance = Literal["bullish", "neutral", "bearish"]


class AgentPromptSpec(BaseModel):
    name: str
    role: str
    output_fields: list[str] = Field(default_factory=list)


class PersonaDefinition(BaseModel):
    """Externalized investment persona loaded from YAML."""

    name: str
    philosophy: str
    preferred_evidence: list[str]
    blind_spots: list[str]
    scoring_rubric: dict[str, float]
    output_schema: dict[str, Any]

    @field_validator("scoring_rubric")
    @classmethod
    def rubric_must_have_positive_weight(cls, value: dict[str, float]) -> dict[str, float]:
        if not value:
            raise ValueError("scoring_rubric must not be empty")
        if any(weight < 0 for weight in value.values()):
            raise ValueError("scoring_rubric weights must be non-negative")
        if sum(value.values()) <= 0:
            raise ValueError("scoring_rubric weights must sum to a positive value")
        return value


class PersonaOpinion(BaseModel):
    """One persona's structured, rule-based first-pass opinion."""

    ticker: str
    persona_name: str
    score: float = Field(ge=0, le=100)
    stance: Stance
    confidence: float = Field(ge=0, le=1)
    evidence: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)


class ConsensusSummary(BaseModel):
    mean_score: float = Field(ge=0, le=100)
    score_std: float = Field(ge=0)
    bullish_count: int = Field(ge=0)
    neutral_count: int = Field(ge=0)
    bearish_count: int = Field(ge=0)
    consensus_score: float = Field(ge=0, le=100)
    disagreement_score: float = Field(ge=0, le=100)


class CouncilResult(BaseModel):
    """Structured persona council output that can be persisted in a future table."""

    ticker: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    opinions: list[PersonaOpinion]
    consensus: ConsensusSummary
    context_keys: list[str] = Field(default_factory=list)
