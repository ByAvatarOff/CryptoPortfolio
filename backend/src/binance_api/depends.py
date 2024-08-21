from fastapi import Depends

from src.binance_api.domain.services.http_service import BinanceService
from src.binance_api.domain.services.ws_service import BinanceWebSocketService
from src.binance_api.controllers.controller import BinanceController
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.portfolio.depends import _get_operation_read_command_repo
from src.auth.models import User
from src.auth.base_config import current_user
from src.binance_api.gateways.binance.binance_http import BinanceAPI, BinanceClient
from src.binance_api.gateways.binance.binance_websockets import BinanceWebSocketClient


def _get_binance_client() -> BinanceClient:
    return BinanceClient()


def _get_binance_ws_client() -> BinanceWebSocketClient:
    return BinanceWebSocketClient()


def _get_binance_api(client: BinanceClient = Depends(_get_binance_client)) -> BinanceAPI:
    return BinanceAPI(client=client)


def _get_binance_service(
        repo: OperationReadCommandRepo = Depends(_get_operation_read_command_repo),
        binance_api: BinanceAPI = Depends(_get_binance_api),
) -> BinanceService:
    return BinanceService(
        binance_api=binance_api,
        operation_read_command_repo = repo,
    )


def get_binance_controller(
        user: User = Depends(current_user),
        service: BinanceService = Depends(_get_binance_service),
) -> BinanceController:
    return BinanceController(
        user=user,
        binance_service=service
    )


def get_binance_ws_service(
        repo: OperationReadCommandRepo = Depends(_get_operation_read_command_repo),
        binance_ws_client: BinanceWebSocketClient = Depends(_get_binance_ws_client),
) -> BinanceWebSocketService:
    return BinanceWebSocketService(
        operation_read_command_repo=repo,
        binance_ws_client=binance_ws_client,
    )