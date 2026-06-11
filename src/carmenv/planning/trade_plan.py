from datetime import date

from pydantic import BaseModel, Field


class TradePlan(BaseModel):
    date: date
    ticker: str
    trade_type: str = "swing"
    entry_zone_low: float = Field(gt=0)
    entry_zone_high: float = Field(gt=0)
    stop_loss: float = Field(gt=0)
    take_profit_1: float = Field(gt=0)
    take_profit_2: float = Field(gt=0)
    invalid_condition: str
    holding_period_days: int = Field(gt=0)
    position_size_pct: float = Field(ge=0, le=100)
    reason: str
