from auth.base_config import current_user
from auth.models import User
from binance_api.binance_schemas import TimeFramePercentChanges
from binance_api.binance_service import BinanceService, BinanceWebSocketService
from fastapi import APIRouter, Depends, WebSocket, status

binance_router = APIRouter(
    prefix='/api/binance',
    tags=['binanceApi']
)


@binance_router.get('/list_all_tickers/',
                    status_code=status.HTTP_200_OK
                    )
async def list_all_tickers(
        binance_service: BinanceService = Depends()
) -> list[str]:
    """Return list binance allow ticker pair with USDT"""
    return await binance_service.get_all_symbols()


@binance_router.get('/ticker_price_changed/',
                    response_model=TimeFramePercentChanges,
                    status_code=status.HTTP_200_OK
                    )
async def ticker_price_changed(
        binance_service: BinanceService = Depends(),
        user: User = Depends(current_user),
) -> TimeFramePercentChanges:
    """Return list binance allow ticker pair with USDT"""
    return await binance_service.ticker_price_changes(user_id=user.id)


@binance_router.websocket('/ws/{access_token}')
async def ws_timeframe_changes(
        access_token: str,
        websocket: WebSocket,
        binance_service: BinanceWebSocketService = Depends()
):
    """Return User ticker prices use WebSocket"""
    await binance_service.ws_timeframe_changes(websocket=websocket, access_token=access_token)
