from fastapi import WebSocket
from auth.utils import decode_access
import asyncio
import websockets
import json

from config import BINANCE_WS_TICKER_PRICE_URL


class WSConnectionManager:
    """WebSocket Connection Manager"""
    def __init__(self, access_token: str):
        self.active_connections: list[WebSocket] = []
        self.access_token = access_token
        self.user_id = None

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
    async def create_ws_url(self, list_tickers) -> str:
        """Create sw url use user tickers"""
        timeframe = '1h'
        base_url = BINANCE_WS_TICKER_PRICE_URL
        for ticker in list_tickers:
            base_url += f'{ticker.lower()}@kline_{timeframe}/'
        return base_url[:-1]

    async def get_ticker_timeframe_prices(self, list_tickers, manager, websocket):
        """Connect to binance ws and return ticker prices"""
        ws_url = await self.create_ws_url(list_tickers)
        async with websockets.connect(ws_url) as ws:
            while True:
                result = await ws.recv()
                result_json = json.loads(result)
                ticker_price = {
                    "ticker": result_json.get('data').get('s'),
                    "price": result_json.get('data').get('k').get('c'),
                }
                await manager.send_json_message(ticker_price, websocket)
