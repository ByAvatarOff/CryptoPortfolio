from pydantic import BaseModel, field_validator
from datetime import datetime


class PortfolioSchema(BaseModel):
    id: int
    ticker: str
    amount: float
    price: float
    add_date: datetime
    type: str
    user_id: int


class PortfolioCreateSchema(BaseModel):
    ticker: str
    amount: float
    price: float
    type: str
    user_id: int

    @field_validator('type')
    def type_validation(cls, type: str):
        if type.lower() not in ['buy', 'sell']:
            raise ValueError("Invalid type only buy or sell")
        return type


class TickersListSchema(BaseModel):
    ticker: str


class ListTickersPrice(BaseModel):
    symbol: str
    price: float


class ListInvestmentSchema(BaseModel):
    ticker: str
    amount_difference: float
    price_difference: float
    avg_price: float
