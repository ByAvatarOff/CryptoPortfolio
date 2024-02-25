from pydantic import BaseModel


class ListTickersPrice(BaseModel):
    symbol: str
    price: float
