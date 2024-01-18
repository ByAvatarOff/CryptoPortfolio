from .models import portfolio
from sqlalchemy import select, case, func, RowMapping
import aiohttp
from config import SECRET_AUTH
from jose import jwt, JWTError
import json
from .schemas import ListTickersPrice, PortfolioSchema
from sqlalchemy.ext.asyncio import AsyncSession
from functools import reduce


async def decode_access(token: str) -> int:
    try:
        payload = jwt.decode(token, key=SECRET_AUTH, algorithms=["HS256"], audience="fastapi-users:auth")
        return payload.get('sub')
    except JWTError:
        return 0


async def get_user_portfolio(user_id: int, session: AsyncSession) -> list[PortfolioSchema]:
    """
    All operation in user portfolio
    """
    stmt = select(portfolio).where(portfolio.c.user_id == user_id)
    result = await session.execute(stmt)
    return result.all()


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


async def get_ticker_price(list_ticker: list[str]) -> list[ListTickersPrice]:
    """
    Get prices tickers from list_ticker use binance api
    Return object: [{'symbol': 'BNBUSDT', 'price': '317.40000000'}]
    """
    url = f'https://api.binance.com/api/v3/ticker/price?symbols={str(json.dumps(list_ticker)).replace(" ", "")}'
    response = await get_data_from_api_endpoint(url)
    return response


async def get_difference_type(session: AsyncSession, user_id: int) -> list[RowMapping]:
    """
    Find difference
    """
    stmt = select(
        portfolio.c.ticker,

        (func.sum(case((portfolio.c.type == 'buy', portfolio.c.amount), else_=0)) -
         func.sum(case((portfolio.c.type == 'sell', portfolio.c.amount), else_=0)))
        .label('amount_difference'),

        (func.sum(case((portfolio.c.type == 'buy', portfolio.c.amount * portfolio.c.price), else_=0)) -
         func.sum(case((portfolio.c.type == 'sell', portfolio.c.amount * portfolio.c.price), else_=0)))
        .label('price_difference'),

        ((func.sum(case((portfolio.c.type == 'buy', portfolio.c.amount * portfolio.c.price), else_=0)) -
          func.sum(case((portfolio.c.type == 'sell', portfolio.c.amount * portfolio.c.price), else_=0))) /
         case((func.sum(case((portfolio.c.type == 'buy', portfolio.c.amount), else_=0)) -
               func.sum(case((portfolio.c.type == 'sell', portfolio.c.amount), else_=0)) == 0, 1),
              else_=func.sum(case((portfolio.c.type == 'buy', portfolio.c.amount), else_=0)) -
                    func.sum(case((portfolio.c.type == 'sell', portfolio.c.amount), else_=0))))
        .label('avg_price')
    ).where(portfolio.c.user_id == user_id).group_by(portfolio.c.ticker).order_by(portfolio.c.ticker)
    result = await session.execute(stmt)
    return result.mappings().all()


async def update_current_ticker_price(list_difference: list[RowMapping], list_dict_prices: list[ListTickersPrice]):
    """
    Get from binance api current prices tickers, and return list with price ticker * amount ticker
    """
    list_dict_prices = sorted(list_dict_prices, key=lambda x: x.get('symbol'))
    for (obj, amount) in zip(list_dict_prices, list_difference):
        obj.update({'symbol': obj.get('symbol'),
                    "price": float(obj.get('price')) * float(amount.get('amount_difference'))})
    return list_dict_prices


async def compute_all_time_profit(session: AsyncSession, user_id: int):
    """
    Get from binance api current prices tickers, and return list with price ticker * amount ticker
    """
    list_difference = await get_difference_type(session, user_id)
    list_ticker_current_price = await get_ticker_price(list(map(lambda obj: obj.get('ticker'), list_difference)))
    stmt = select(func.sum(portfolio.c.price * portfolio.c.amount).label('total_price')).where(portfolio.c.user_id == user_id)
    result = await session.execute(stmt)
    user_active_price = result.mappings().all()[0]
    current_active_price = await update_current_ticker_price(list_difference, list_ticker_current_price)

    return sum(map(lambda x: x.get('price', 0), current_active_price)) - user_active_price.get('total_price', 0)























