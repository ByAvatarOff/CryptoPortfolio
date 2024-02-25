from fastapi import APIRouter, Depends
from starlette import status

from binance_api.binance_service import BinanceService

binance_router = APIRouter(
    prefix="/api/binance",
    tags=["binanceApi"]
)


@binance_router.get("/list_all_tickers/",
                    status_code=status.HTTP_200_OK)
async def list_all_tickers(
        binance_service: BinanceService = Depends()
) -> list[str]:
    """
    Return list binance allow ticker pair with USDT
    """
    return await binance_service.get_all_symbols()


# async def create_ws_url(list_tickers: list) -> str:
#     timeframe = '1h'
#     base_url = 'wss://stream.binance.com:443/stream?streams='
#     for ticker in list_tickers:
#         base_url += f'{ticker.get("ticker")}@kline_{timeframe}/'
#     return base_url


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
#         await asyncio.sleep(3)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# @portfolio_router.websocket("/ws/{token}")
# async def websocket_endpoint(token: str, websocket: WebSocket, session: AsyncSession = Depends(get_async_session)):

#     manager = ConnectionManager()
#     await manager.connect(websocket)
#     try:
#         while True:
#             await manager.send_personal_message({"text": "new text"}, websocket)
#         # user_id: int = await decode_access(token)
#         # if not user_id:
#         #     return await websocket.close(reason='Not authorize')
#         # list_tickers = await get_user_portfolio_unique_tiker(int(user_id), session)
#         # ws_url = await create_ws_url(list_tickers)
#         # # list_dict_prices = list_tickers.copy()
#         # async with websockets.connect(ws_url[:-1]) as ws:
#         #     while True:
#         #         result = await ws.recv()
#         #         result_json = json.loads(result)
#         #         prices = {
#         #             "nee": "53453534"
#         #         }
#         #         # prices: list[dict] = await update_current_ticker_price(result_json.get('data').get('s'),
#         #         #                                                        result_json.get('data').get('k').get('c'),
#         #         #                                                        list_dict_prices)

#         #         await websocket.send_json(json.dumps(prices))
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)