from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_async_session
from starlette import status

from .schemas import PortfolioSchema, PortfolioCreateSchema
from .models import portfolio
from sqlalchemy import select, insert, delete, func, case
from auth.base_config import current_user
from auth.models import User, user
from .utils import get_user_portfolio, \
    decode_access, get_all_symbols, get_ticker_price, \
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
                             user: User = Depends(current_user)) -> list[PortfolioSchema]:
    """
    Return list all user operation in portfolio
    """
    return await get_user_portfolio(user.id, session)


@portfolio_router.post("/create_operation/",
                       response_model=list[PortfolioSchema],
                       status_code=status.HTTP_201_CREATED)
async def add_operation(new_operation: PortfolioCreateSchema,
                        session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)) -> list[PortfolioSchema] | JSONResponse:
    """
    Create operation in portfolio
    Check if
    """
    user_id: int = user.id
    stmt = select(func.coalesce(func.sum(case((portfolio.c.type == 'buy', portfolio.c.amount), else_=0)) -
                                func.sum(case((portfolio.c.type == 'sell', portfolio.c.amount), else_=0)), 0).label(
        'diff_amount')) \
        .where((portfolio.c.user_id == user_id) &
               (portfolio.c.ticker == new_operation.ticker))
    result = (await session.execute(stmt)).mappings().all()[0].get('diff_amount')
    if result - new_operation.amount < 0 and new_operation.type != 'buy':
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": 'You cant to sell more than buy'},
        )
    new_operation.user_id = user.id
    stmt = insert(portfolio).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return await get_user_portfolio(user.id, session)


@portfolio_router.delete("/delete_operation/{operation_id}/",
                         response_model=list[PortfolioSchema],
                         status_code=status.HTTP_200_OK)
async def delete_operation(operation_id: int,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)) -> list[PortfolioSchema]:
    """
    Delete user operation in portfolio and return new list with operation
    """
    stmt = delete(portfolio).where(portfolio.c.id == operation_id)
    await session.execute(stmt)
    await session.commit()
    return await get_user_portfolio(user.id, session)


@portfolio_router.get("/all_investments/", status_code=status.HTTP_200_OK)
async def list_all_investments(session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user)):
    return await get_difference_type(session, user.id)


@portfolio_router.get("/porfolio_operation_sum/",
                      status_code=status.HTTP_200_OK)
async def portfolio_operation_sum(session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_user)):
    """
    Form list with amount tickers with buy and sell
    After request to binance with unique tickers and it return price there tickers
    And return result list[dict] with price * amount
    """
    list_difference = await get_difference_type(session, user.id)
    list_ticker_current_price = await get_ticker_price(list(map(lambda obj: obj.get('ticker'), list_difference)))

    result_ticker_prices = await update_current_ticker_price(list_difference, list_ticker_current_price)
    print(json.dumps(result_ticker_prices))
    return json.dumps(result_ticker_prices)


@portfolio_router.get("/all_time_profit/",
                      status_code=status.HTTP_200_OK)
async def all_time_profit(session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    """
    Return user profit user price actives - current price actives
    """
    return await compute_all_time_profit(session, user.id)