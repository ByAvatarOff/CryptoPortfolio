from pydantic import BaseModel, Field


class ListTickersPrice(BaseModel):
    symbol: str
    price: float


class TickerChanges(BaseModel):
    ticker: str
    percent: str


class TimeFramePercentChanges(BaseModel):
    data: dict[str, list[TickerChanges]] | None = Field(default_factory=dict)
