from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class PortfolioSchema(BaseModel):
    """Portfolio Read Schema"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    ticker: str
    amount: float
    price: float
    add_date: datetime
    type: str
    user_id: int


class PortfolioCreateSchema(BaseModel):
    """Portfolio Read Schema"""
    ticker: str
    amount: float
    price: float
    type: str
    user_id: int

    @field_validator('type')
    def type_validation(cls, type: str):
        """Validation type portfolio"""
        if type.lower() not in ['buy', 'sell']:
            raise ValueError('Invalid type only buy or sell')
        return type
