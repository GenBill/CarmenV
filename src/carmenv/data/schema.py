from datetime import date
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SymbolInfo(BaseModel):
    ticker: str
    name: str
    exchange: str
    asset_type: str = "stock"
    currency: str = "USD"
    sector: str | None = None
    industry: str | None = None
    is_active: bool = True
    list_date: date | None = None


class DailyBar(BaseModel):
    date: date
    ticker: str
    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)
    volume: float = Field(ge=0)
    amount: float = Field(ge=0)
    adj_factor: float | None = None

    @field_validator("high")
    @classmethod
    def high_is_positive(cls, value: float) -> float:
        return value


class TechnicalFeatures(BaseModel):
    date: date
    ticker: str
    close: float
    ma5: float | None = None
    ma10: float | None = None
    ma20: float | None = None
    ma60: float | None = None
    return_1d: float | None = None
    return_5d: float | None = None
    return_20d: float | None = None
    volatility_20d: float | None = None
    amount_ma20: float | None = None
    atr_14: float | None = None
    relative_strength_20d: float | None = None


class CandidateRecord(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    date: date
    ticker: str
    source: str
    rank: int
    pattern_type: str
    close: float
    reason: str
    feature_snapshot: dict[str, Any] = Field(default_factory=dict)
