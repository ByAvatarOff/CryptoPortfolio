from aiohttp import ClientSession
from config import BINANCE_LIST_TICKER_PRICE_URL, BINANCE_TICKER_CURRENT_PRICE_TIMEFRAME
from fastapi import Depends, HTTPException


class BinanceHTTPSession:
    """Create session For Binance"""
    @staticmethod
    async def async_http_session():
        """create binance async session"""
        async with ClientSession(base_url='https://api.binance.com') as session:
            yield session


class BinanceHTTPMethods:
    """Binance http methods"""

    def __init__(self, binance_session: ClientSession = Depends(BinanceHTTPSession.async_http_session)):
        self.binance_session = binance_session

    async def get(self, url: str, params=None) -> list[dict]:
        """Get method"""
        if not params:
            return await (await self.binance_session.get(url=url)).json()
        return await (await self.binance_session.get(url=url, params=params)).json()


class BinanceAPI(BinanceHTTPMethods):
    async def get_ticker_current_price(
            self,
            list_tickers,
            period=BINANCE_TICKER_CURRENT_PRICE_TIMEFRAME
    ) -> list[dict]:
        """Get prices tickers from list_tickers use binance api"""
        response = await self.get(
            url=f'{BINANCE_LIST_TICKER_PRICE_URL}{list_tickers}&type=MINI&windowSize={period}'
        )
        if 'code' in response:
            raise HTTPException(status_code=400, detail='Invalid period')
        return response
