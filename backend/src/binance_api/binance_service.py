from binance_api.binance_http import BinanceAPI, BinanceHTTPMethods
from binance_api.binance_schemas import TimeFramePercentChanges
from binance_api.binance_utils import BinanceTransformer
from binance_api.binance_websockets import BinanceWebSocketMethods, WSConnectionManager
from config import BINANCE_TICKER_PRICE_URL
from fastapi import Depends, WebSocket, WebSocketDisconnect
from investment.investment_utils import InvestmentUtils
from portfolio.portfolio_repo import PortfolioRepo


class BinanceService:
    """Binance service"""

    def __init__(
            self,
            binance_request: BinanceHTTPMethods = Depends(),
            portfolio_repo: PortfolioRepo = Depends(),
            binance_transformer: BinanceTransformer = Depends(),
            investment_utils: InvestmentUtils = Depends(),
            binance_api: BinanceAPI = Depends(),
    ):
        self.binance_request = binance_request
        self.portfolio_repo = portfolio_repo
        self.investment_utils = investment_utils
        self.binance_transformer = binance_transformer
        self.binance_api = binance_api

    async def get_all_symbols(self) -> list[str]:
        """
        Request to binance api and get allow ticker pair with USDT
        Return list tickers
        """
        response = await self.binance_request.get(BINANCE_TICKER_PRICE_URL)
        if response:
            return [data.get('symbol') for data in response if 'USDT' in data.get('symbol')]
        return []

    async def ticker_price_changes(
            self,
            user_id: int
    ) -> TimeFramePercentChanges:
        """
        Get user unique tickers
        request to binance with timeframe
        return ticker price change
        """
        timeframes = ['1d', '7d']
        tm_ticker_prices = {}
        list_tickers = await self.investment_utils.prepare_tickers_for_get_price(
            await self.portfolio_repo.get_unique_user_ticker(user_id=user_id)
        )

        for timeframe in timeframes:
            price_change = await self.binance_transformer.transform_responce_to_profit_persent(
                await self.binance_api.get_ticker_current_price(
                    list_tickers=list_tickers,
                    period=timeframe
                ))
            tm_ticker_prices.update({
                f'timeframe_{timeframe}': price_change
            })
        return TimeFramePercentChanges(**tm_ticker_prices)


class BinanceWebSocketService:
    """Binance WebSocket Service"""

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
                await self.binance_websocket.get_ticker_prices(
                    list_tickers=list_tickers,
                    manager=manager,
                    websocket=websocket,
                )

        except WebSocketDisconnect:
            manager.disconnect(websocket)
