import asyncio
import json

import websockets
from src.auth.utils import decode_access
from src.core.settings import settings
from fastapi import WebSocket


class WSConnectionManager:
    """WebSocket Connection Manager"""

    def __init__(self, access_token: str):
        self.active_connections: list[WebSocket] = []
        self.access_token = access_token
        self.user_id = 0

    async def connect(self, websocket: WebSocket):
        """Connect to ws"""
        user_id = await decode_access(self.access_token)
        if not user_id:
            self.active_connections.remove(websocket)
        self.user_id = int(user_id)
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """DisConnect from ws"""
        self.active_connections.remove(websocket)

    async def send_json_message(self, message: str, websocket: WebSocket):
        """Send message use ws"""
        await websocket.send_json(message)
        await asyncio.sleep(2)


class BinanceWebSocketMethods:
    """Binance WebSocket Methods"""
    async def create_ws_url(self, list_tickers) -> str:
        """Create sw url use user tickers"""
        base_url = settings.app.binance_ws_ticker_price_url
        for ticker in list_tickers:
            base_url += f'{ticker.lower()}@kline_{settings.app.binance_ticker_current_price_timeframe}/'
        return base_url[:-1]

    async def get_ticker_prices(self, list_tickers, manager, websocket):
        """Connect to binance ws and return ticker prices"""
        ws_url = await self.create_ws_url(list_tickers)
        async with websockets.connect(ws_url) as ws:
            while True:
                result = await ws.recv()
                result_json = json.loads(result)
                ticker_price = {
                    'ticker': result_json.get('data').get('s'),
                    'price': result_json.get('data').get('k').get('c'),
                }
                await manager.send_json_message(ticker_price, websocket)
