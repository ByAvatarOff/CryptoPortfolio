from pydantic import BaseModel


class ListTickersPrice(BaseModel):
    symbol: str
    price: float


class Ticker(BaseModel):
    ticker: str
    percent: str


class TimeFramePercentChanges(BaseModel):
    timeframe_1d: list[Ticker]
    timeframe_7d: list[Ticker]
