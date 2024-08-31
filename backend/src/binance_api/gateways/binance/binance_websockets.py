import json
import websockets

from src.core.settings import settings


class BinanceWebSocketClient:
    def __init__(self) -> None:
        self.base_binance_ws_url = settings.app.binance_ws_base_url

    async def create_ws_url(self, list_tickers: list[dict]) -> str:
        base_url = settings.app.binance_ws_ticker_price_url
        for ticker in list_tickers:
            base_url += f'{ticker.lower()}@kline_{settings.app.binance_ticker_current_price_timeframe}/'
        return base_url[:-1]

    async def get_ticker_prices(self, list_tickers: list[dict], manager, websocket):
        ws_url = await self.create_ws_url(list_tickers)
        async with websockets.connect(self.base_binance_ws_url + ws_url) as ws:
            while True:
                result = await ws.recv()
                result_json = json.loads(result)
                ticker_price = {
                    'ticker': result_json.get('data').get('s'),
                    'price': result_json.get('data').get('k').get('c'),
                }
                await manager.send_json_message(ticker_price, websocket)
