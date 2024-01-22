from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from sqlalchemy import select, case, func, RowMapping
from collections.abc import Sequence
from starlette import status
from jose import jwt, JWTError
import aiohttp

from portfolio.models import Portfolio
from config import SECRET_AUTH
from portfolio.schemas import ListTickersPrice, PortfolioCreateSchema
import json


async def decode_access(token: str) -> int:
    try:
        payload = jwt.decode(token, key=SECRET_AUTH, algorithms=["HS256"], audience="fastapi-users:auth")
        return payload.get('sub')
    except JWTError:
        return 0


async def get_user_portfolio(user_id: int, session: AsyncSession) -> Sequence[RowMapping]:
    """
    All operation in user portfolio
    """
    stmt = select(Portfolio).where(Portfolio.user_id == user_id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_data_from_api_endpoint(url: str, params=None) -> list[any] | dict:
    """
    Create aiohttp session and send request to url
    Return json response
    """
    async with aiohttp.ClientSession() as session:
        response = await session.get(url, params=params)
        if response.status != 200:
            return {}
        return await response.json()


async def get_all_symbols() -> list[str]:
    """
    Request to binance api and get allow ticker pair with USDT
    Return list tickers
    """
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = await get_data_from_api_endpoint(url)
    if response:
        return [data.get('symbol') for data in response if 'USDT' in data.get('symbol')]
    return []


async def get_ticker_current_price(list_difference) -> list[ListTickersPrice]:
    """
    Get prices tickers from list_ticker use binance api
    Return object: [{'symbol': 'BNBUSDT', 'price': '317.40000000'}]
    """
    list_tickers = list(map(lambda obj: obj.get('ticker'), list_difference))
    url = f'https://api.binance.com/api/v3/ticker/price?symbols={str(json.dumps(list_tickers)).replace(" ", "")}'
    response = await get_data_from_api_endpoint(url)
    return response


async def check_diff_amount(user_id: int,
                            session: AsyncSession,
                            new_operation: PortfolioCreateSchema
                            ) -> JSONResponse | bool:
    """
    Check diff amount between ticker with type buy and sell
    """
    stmt = select(func.coalesce(func.sum(case((Portfolio.type == 'buy', Portfolio.amount), else_=0)) -
                                func.sum(case((Portfolio.type == 'sell', Portfolio.amount), else_=0)), 0)
                  .label('diff_amount')) \
        .where((Portfolio.user_id == user_id) &
               (Portfolio.ticker == new_operation.ticker))
    record = await session.execute(stmt)
    result = record.scalars().first()
    if result - new_operation.amount < 0 and new_operation.type != 'buy':
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": 'You cant to sell more than buy'},
        )
    return True


async def get_difference_type(session: AsyncSession, user_id: int) -> Sequence[RowMapping]:
    """
    Find difference
    """
    stmt = select(
        Portfolio.ticker,

        (func.sum(case((Portfolio.type == 'buy', Portfolio.amount), else_=0)) -
         func.sum(case((Portfolio.type == 'sell', Portfolio.amount), else_=0)))
        .label('amount_difference'),

        (func.sum(case((Portfolio.type == 'buy', Portfolio.amount * Portfolio.price), else_=0)) -
         func.sum(case((Portfolio.type == 'sell', Portfolio.amount * Portfolio.price), else_=0)))
        .label('price_difference'),

        ((func.sum(case((Portfolio.type == 'buy', Portfolio.amount * Portfolio.price), else_=0)) -
          func.sum(case((Portfolio.type == 'sell', Portfolio.amount * Portfolio.price), else_=0))) /
         case((func.sum(case((Portfolio.type == 'buy', Portfolio.amount), else_=0)) -
               func.sum(case((Portfolio.type == 'sell', Portfolio.amount), else_=0)) == 0, 1),
              else_=func.sum(case((Portfolio.type == 'buy', Portfolio.amount), else_=0)) -
                    func.sum(case((Portfolio.type == 'sell', Portfolio.amount), else_=0))))
        .label('avg_price')
    ).where(Portfolio.user_id == user_id).group_by(Portfolio.ticker).order_by(Portfolio.ticker)
    result = await session.execute(stmt)
    return result.mappings().all()


async def update_current_ticker_price(list_difference: Sequence[RowMapping],
                                      list_dict_prices: list[ListTickersPrice]) -> list[ListTickersPrice]:
    """
    Get from binance api current prices tickers, and return list with price ticker * amount ticker
    """
    list_dict_prices: list = sorted(list_dict_prices, key=lambda x: x.get('symbol'))
    for (obj, amount) in zip(list_dict_prices, list_difference):
        obj.update({'symbol': obj.get('symbol'),
                    "price": float(obj.get('price')) * float(amount.get('amount_difference'))})
    return list_dict_prices


async def compute_all_time_profit(session: AsyncSession, user_id: int) -> float:
    """
    Get from binance api current prices tickers, and return list with price ticker * amount ticker
    """
    list_difference = await get_difference_type(session, user_id)
    list_ticker_current_price = await get_ticker_current_price(list_difference)
    stmt = select(func.coalesce(func.sum(Portfolio.price * Portfolio.amount), 0)
                  .label('total_price')).where(Portfolio.user_id == user_id)
    result = await session.execute(stmt)
    user_active_price = result.mappings().first()
    current_active_price = await update_current_ticker_price(list_difference, list_ticker_current_price)
    return sum(map(lambda x: x.get('price', 0), current_active_price)) - user_active_price.get('total_price', 0)
