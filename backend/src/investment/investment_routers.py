from fastapi import APIRouter, Depends
from starlette import status

from investment.investment_schemas import InvestmentSchema, OperationSumSchema, AllTimeProfitSchema
from auth.base_config import current_user
from auth.models import User
from investment.investment_service import InvestmentService


investment_router = APIRouter(
    prefix="/api/investment",
    tags=["investment"]
)


@investment_router.get("/all_investments/",
                       response_model=list[InvestmentSchema],
                       status_code=status.HTTP_200_OK)
async def list_investments(
        user: User = Depends(current_user),
        investment_service: InvestmentService = Depends(InvestmentService),
) -> list[InvestmentSchema]:
    """List user operation in investment"""
    return await investment_service.list_investments(user_id=user.id)


@investment_router.get("/porfolio_operation_sum/",
                       response_model=list[OperationSumSchema],
                       status_code=status.HTTP_200_OK)
async def sum_operations(
        user: User = Depends(current_user),
        investment_service: InvestmentService = Depends(InvestmentService),
) -> list[OperationSumSchema]:
    """
    Form list with amount tickers with buy and sell
    After request to binance with unique tickers, and it returns price there tickers
    And return result list[dict] with price * amount
    """
    return await investment_service.sum_operations(user_id=user.id)


@investment_router.get("/all_time_profit/{period}/",
                       response_model=AllTimeProfitSchema,
                       status_code=status.HTTP_200_OK)
async def all_time_profit(
        period: str,
        user: User = Depends(current_user),
        investment_service: InvestmentService = Depends(InvestmentService),
) -> AllTimeProfitSchema:
    """Return user profit user price actives - current price actives"""
    return await investment_service.all_time_profit(user_id=user.id, period=period)
