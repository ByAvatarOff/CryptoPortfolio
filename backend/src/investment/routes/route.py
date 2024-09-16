from fastapi import APIRouter, Depends
from src.investment.schemas.schema import (
    InvestmentSchema,
    OperationSumSchema,
    AllTimeProfitSchema,
)
from src.investment.schemas.enum import PeriodTimeframeEnum
from src.investment.controllers.controller import InvestmentController
from src.investment.depends import get_investment_controller
from starlette import status

investment_router = APIRouter(
    prefix='/api/investment',
    tags=['investment']
)


@investment_router.get(
    '/list_tickers_stat/{portfolio_id}/',
    response_model=list[InvestmentSchema],
    status_code=status.HTTP_200_OK
)
async def list_tickers_stat(
        portfolio_id: int,
        controller: InvestmentController = Depends(get_investment_controller),
) -> list[dict]:
    return await controller.list_tickers_stat(portfolio_id=portfolio_id)


@investment_router.get(
    '/sum_operations/',
    response_model=list[OperationSumSchema],
    status_code=status.HTTP_200_OK
)
async def sum_operations(
        controller: InvestmentController = Depends(get_investment_controller),
) -> list[dict]:
    return await controller.sum_operations()


@investment_router.get(
    '/all_time_profit/{period}/',
    response_model=AllTimeProfitSchema,
    status_code=status.HTTP_200_OK
)
async def all_time_profit(
        period: PeriodTimeframeEnum,
        controller: InvestmentController = Depends(get_investment_controller),
) -> AllTimeProfitSchema:
    return await controller.all_time_profit(period=period)
