from fastapi import Depends
from binance_api.binance_utils import BinanceHTTPMethods
from config import BINANCE_TICKER_PRICE_URL


class BinanceService:
    """Binance service"""
    def __init__(self, binance_request: BinanceHTTPMethods = Depends()):
        self.binance_request = binance_request

    async def get_all_symbols(self) -> list[str]:
        """
        Request to binance api and get allow ticker pair with USDT
        Return list tickers
        """
        response = await self.binance_request.get(BINANCE_TICKER_PRICE_URL)
        if response:
            return [data.get('symbol') for data in response if 'USDT' in data.get('symbol')]
        return []