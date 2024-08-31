from fastapi import WebSocket, WebSocketDisconnect
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.binance_api.gateways.binance.binance_websockets import BinanceWebSocketClient
from src.core.services.ws_connection_manager import WSConnectionManager


class BinanceWebSocketService:

    def __init__(
            self,
            operation_read_command_repo: OperationReadCommandRepo,
            binance_ws_client: BinanceWebSocketClient,
    ):
        self.operation_read_command_repo = operation_read_command_repo
        self.binance_ws_client = binance_ws_client

    async def ws_timeframe_changes(
            self,
            websocket: WebSocket,
            access_token: str
    ):
        manager = WSConnectionManager(access_token=access_token)
        await manager.connect(websocket)
        list_tickers = await self.operation_read_command_repo.get_unique_user_ticker(user_id=manager.user_id)
        try:
            while True:
                await self.binance_ws_client.get_ticker_prices(
                    list_tickers=list_tickers,
                    manager=manager,
                    websocket=websocket,
                )

        except WebSocketDisconnect:
            manager.disconnect(websocket)