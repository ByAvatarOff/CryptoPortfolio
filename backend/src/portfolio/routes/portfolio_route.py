from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from src.portfolio.schemas.schema import PortfolioSchema, PortfolioCreateSchema
from starlette import status
from src.portfolio.depends import get_portfolio_controller

if TYPE_CHECKING:
    from src.portfolio.models.models import Portfolio
    from src.portfolio.controllers.portfolio_controller import PortfolioController


portfolio_router = APIRouter(
    prefix='/api/portfolio',
    tags=['portfolio']
)


@portfolio_router.post(
    '/',
    response_model=PortfolioSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(
        new_portfolio: PortfolioCreateSchema,
        controller: PortfolioController = Depends(get_portfolio_controller),
) -> Portfolio:
    return await controller.create(new_portfolio=new_portfolio)


@portfolio_router.get(
    '/',
    response_model=list[PortfolioSchema],
    status_code=status.HTTP_200_OK
)
async def list(
        controller: PortfolioController = Depends(get_portfolio_controller),
) -> list[Portfolio]:
    return await controller.list()



@portfolio_router.delete(
    '/{portfolio_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        portfolio_id: int,
        controller: PortfolioController = Depends(get_portfolio_controller),
):
    await controller.delete(
        portfolio_id=portfolio_id
    )
