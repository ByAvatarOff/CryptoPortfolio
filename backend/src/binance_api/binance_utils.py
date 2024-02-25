from aiohttp import ClientSession
from fastapi import Depends, HTTPException
from config import BINANCE_LIST_TICKER_PRICE_URL
from jose import jwt, JWTError
from config import SECRET_AUTH


# async def decode_access(token: str) -> int:
#     try:
#         payload = jwt.decode(token, key=SECRET_AUTH, algorithms=["HS256"], audience="fastapi-users:auth")
#         return payload.get('sub')
#     except JWTError:
#         return None


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

    async def get(self, url: str, params: dict = None):
        """Get method"""
        if not params:
            return await (await self.binance_session.get(url=url)).json()
        return await (await self.binance_session.get(url=url, params=params)).json()


class BinanceAPI(BinanceHTTPMethods):
    async def get_ticker_current_price(self, list_tickers, period='1m') -> list[dict]:
        """Get prices tickers from list_tickers use binance api"""
        response = await self.get(
            url=f'{BINANCE_LIST_TICKER_PRICE_URL}{list_tickers}&type=MINI&windowSize={period}'
        )
        if 'code' in response:
            raise HTTPException(status_code=400, detail='Invalid period')
        return response