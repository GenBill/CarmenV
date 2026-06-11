from datetime import date

from pydantic import BaseModel, Field


class AgentScore(BaseModel):
    date: date
    ticker: str
    technical_score: float = Field(ge=0, le=100)
    narrative_score: float = Field(ge=0, le=100)
    fundamental_score: float = Field(ge=0, le=100)
    risk_score: float = Field(ge=0, le=100)
    liquidity_score: float = Field(ge=0, le=100)
    final_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    summary: str
    raw_response: str | None = None
