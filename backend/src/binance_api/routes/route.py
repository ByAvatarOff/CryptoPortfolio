from fastapi import APIRouter, Depends, WebSocket, status

from src.binance_api.depends import get_binance_controller, get_binance_ws_service
from src.binance_api.controllers.controller import BinanceController
from src.binance_api.domain.services.ws_service import BinanceWebSocketService
from src.binance_api.schemas.schema import TimeFramePercentChanges

binance_router = APIRouter(
    prefix='/api/binance',
    tags=['binanceApi']
)


@binance_router.get(
    '/list_all_tickers/',
    status_code=status.HTTP_200_OK
)
async def list_all_tickers(
        binance_controller: BinanceController = Depends(get_binance_controller)
) -> list[str]:
    return await binance_controller.list_all_tickers()


@binance_router.get(
    '/ticker_price_changed/{portfolio_id}',
    response_model=TimeFramePercentChanges,
    status_code=status.HTTP_200_OK
)
async def ticker_price_changed(
        portfolio_id: int,
        binance_controller: BinanceController = Depends(get_binance_controller)
) -> TimeFramePercentChanges:
    return await binance_controller.ticker_price_changes(portfolio_id=portfolio_id)


@binance_router.websocket('/ws/{access_token}')
async def ws_timeframe_changes(
        access_token: str,
        websocket: WebSocket,
        binance_service: BinanceWebSocketService = Depends(get_binance_ws_service)
):
    await binance_service.ws_timeframe_changes(websocket=websocket, access_token=access_token)
