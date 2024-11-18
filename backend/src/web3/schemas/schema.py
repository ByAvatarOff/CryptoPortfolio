from pydantic import BaseModel
from src.web3.schemas.enum import BlockchainsEnum


class Web3Addresses(BaseModel):
    address: str
    blockchain: BlockchainsEnum