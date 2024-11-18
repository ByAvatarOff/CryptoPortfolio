from datetime import datetime

from pydantic import BaseModel, ConfigDict
from src.portfolio.schemas.enum import OperationTypeEnum


class PortfolioSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image: str
    user_id: int


class PortfolioCreateSchema(BaseModel):
    name: str


class OperationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticker: str
    amount: float
    price: float
    add_date: datetime
    type: OperationTypeEnum
    portfolio_id: int


class OperationCreateSchema(BaseModel):
    ticker: str
    amount: float
    price: float
    type: OperationTypeEnum
    portfolio_id: int
