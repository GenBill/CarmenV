from datetime import date

from pydantic import BaseModel, Field


class AttributionReview(BaseModel):
    date: date
    ticker: str
    actual_bought: bool
    entry_price: float | None = None
    exit_price: float | None = None
    exit_reason: str | None = None
    profit_loss_pct: float | None = None
    attribution_tags: list[str] = Field(default_factory=list)
    manual_comment: str | None = None
