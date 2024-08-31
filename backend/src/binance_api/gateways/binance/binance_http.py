from aiohttp import ClientSession, ContentTypeError

from src.core.exceptions import BinanceApiError
from src.core.settings import settings
from fastapi import HTTPException
from src.binance_api.gateways.binance.abstract import ExternalClient


class BinanceClient(ExternalClient):
    async def get(self, url: str, params: dict =None) -> list[dict]:
        async with ClientSession(base_url=settings.app.binance_base_url) as session:
            try:
                response = await session.get(url=url, params=params)
                return  await response.json()
            except ContentTypeError:
                raise BinanceApiError


class BinanceAPI:
    def __init__(self, client) -> None:
        self.client = client

    async def get_ticker_current_price(
            self,
            list_tickers,
            period=settings.app.binance_ticker_current_price_timeframe
    ) -> list[dict]:
        response = await self.client.get(
            url=f'{settings.app.binance_list_ticker_price_url}{list_tickers}&type=MINI&windowSize={period}'
        )
        if 'code' in response:
            raise HTTPException(status_code=400, detail=response.get("msg"))
        return response

    async def get_list_tickers(self) -> list[str]:
        response = await self.client.get(url=settings.app.binance_ticker_price_url)
        return [data.get('symbol') for data in response if 'USDT' in data.get('symbol')]

    async def get_ticker_info(self, ticker: str) -> dict:
        return await self.client.get(settings.app.binance_ticker_price_url, params={"symbol": ticker})
