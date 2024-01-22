from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_async_session
from starlette import status

from .schemas import PortfolioSchema, PortfolioCreateSchema, ListInvestmentSchema
from portfolio.models import Portfolio
from sqlalchemy import insert, delete
from auth.base_config import current_user
from auth.models import User
from .utils import get_user_portfolio, get_all_symbols, \
    get_ticker_current_price, check_diff_amount, \
    get_difference_type, update_current_ticker_price, \
    compute_all_time_profit
from fastapi.responses import JSONResponse
import json

portfolio_router = APIRouter(
    prefix="/api/portfolio",
    tags=["portfolio"]
)


@portfolio_router.get("/list_all_tickers/", status_code=status.HTTP_200_OK)
async def list_all_tickers() -> list[str]:
    """
    Return list binance allow ticker pair with USDT
    """
    return await get_all_symbols()


@portfolio_router.get("/list_all_operation/",
                      response_model=list[PortfolioSchema],
                      status_code=status.HTTP_200_OK)
async def list_all_operation(session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user)):
    """
    Return list all user operation in portfolio
    """
    return await get_user_portfolio(user.id, session)


@portfolio_router.post("/create_operation/",
                       response_model=list[PortfolioSchema],
                       status_code=status.HTTP_201_CREATED)
async def add_operation(new_operation: PortfolioCreateSchema,
                        session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    """
    Create operation in portfolio
    """
    result: float = await check_diff_amount(user.id, session, new_operation)
    if isinstance(result, JSONResponse):
        return result

    new_operation.user_id = user.id
    stmt = insert(Portfolio).values(new_operation.model_dump())
    await session.execute(stmt)
    await session.commit()
    return await get_user_portfolio(user.id, session)


@portfolio_router.delete("/delete_operation/{operation_id}/",
                         response_model=list[PortfolioSchema],
                         status_code=status.HTTP_200_OK)
async def delete_operation(operation_id: int,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    """
    Delete user operation in portfolio and return new list with operation
    """
    stmt = delete(Portfolio).where(Portfolio.id == operation_id)
    await session.execute(stmt)
    await session.commit()
    return await get_user_portfolio(user.id, session)


@portfolio_router.get("/all_investments/",
                      response_model=list[ListInvestmentSchema],
                      status_code=status.HTTP_200_OK)
async def list_all_investments(session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user)):
    """
    List user operation in investment
    """
    return await get_difference_type(session, user.id)


@portfolio_router.get("/porfolio_operation_sum/",
                      status_code=status.HTTP_200_OK)
async def portfolio_operation_sum(session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_user)):
    """
    Form list with amount tickers with buy and sell
    After request to binance with unique tickers, and it returns price there tickers
    And return result list[dict] with price * amount
    """
    list_difference = await get_difference_type(session, user.id)
    list_ticker_current_price = await get_ticker_current_price(list_difference)
    result_ticker_prices = await update_current_ticker_price(list_difference, list_ticker_current_price)
    return json.dumps(result_ticker_prices)


@portfolio_router.get("/all_time_profit/",
                      status_code=status.HTTP_200_OK)
async def all_time_profit(session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    """
    Return user profit user price actives - current price actives
    """
    return await compute_all_time_profit(session, user.id)