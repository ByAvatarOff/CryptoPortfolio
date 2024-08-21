from pydantic import BaseModel, ConfigDict


class OperationSumSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symbol: str
    price: float


class InvestmentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ticker: str
    amount_difference: float
    price_difference: float
    avg_price: float


class AllTimeProfitSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    profit: float
