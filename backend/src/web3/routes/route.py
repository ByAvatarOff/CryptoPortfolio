from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from src.web3.schemas.schema import Web3PortfolioCreateSchema
from starlette import status
from src.web3.depends import get_web3_controller
from src.portfolio.schemas.schema import PortfolioSchema

if TYPE_CHECKING:
    from src.web3.controllers.web3_controller import Web3Controller


web3_router = APIRouter(
    prefix='/api/web3',
    tags=['web3']
)

@web3_router.post(
    "/web3/create_portfolio/{address}",
    response_model=PortfolioSchema,
    status_code=status.HTTP_200_OK
)
async def create_web3_portfolio(
        web3_data: Web3PortfolioCreateSchema,
        controller: Web3Controller = Depends(get_web3_controller),
):
    return await controller.create_web3_portfolio(web3_data=web3_data)
