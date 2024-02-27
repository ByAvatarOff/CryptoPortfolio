from binance_api.binance_utils import BinanceHTTPMethods
from binance_api.binance_websockets import BinanceWebSocketMethods, WSConnectionManager
from config import BINANCE_TICKER_PRICE_URL
from fastapi import Depends, WebSocket, WebSocketDisconnect
from portfolio.portfolio_repo import PortfolioRepo


class BinanceService:
    """Binance service"""

    def __init__(
            self,
            binance_request: BinanceHTTPMethods = Depends(),
    ):
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


class BinanceWebSocketService:
    def __init__(
            self,
            portfolio_repo: PortfolioRepo = Depends(),
            binance_websocket: BinanceWebSocketMethods = Depends(),
    ):
        self.portfolio_repo = portfolio_repo
        self.binance_websocket = binance_websocket

    async def ws_timeframe_changes(
            self,
            websocket: WebSocket,
            access_token: str
    ):
        """
        Create WS Manager
        Connect to binance ws and return user ticker prices
        """
        manager = WSConnectionManager(access_token=access_token)
        await manager.connect(websocket)
        list_tickers = await self.portfolio_repo.get_unique_user_ticker(user_id=manager.user_id)
        try:
            while True:
                await self.binance_websocket.get_ticker_timeframe_prices(
                    list_tickers=list_tickers,
                    manager=manager,
                    websocket=websocket,
                )

        except WebSocketDisconnect:
            manager.disconnect(websocket)
