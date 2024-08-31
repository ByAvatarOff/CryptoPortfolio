from pydantic import BaseModel
from src.web3.schemas.enum import BlockchainsEnum


class Web3Addresses(BaseModel):
    address: str
    blockchain: BlockchainsEnum


class Web3PortfolioCreateSchema(BaseModel):
    data: list[Web3Addresses]
    name: str