from fastapi import Depends

from src.core.services.thread_pool import ThreadPool
from src.core.services.async_task_pool import AsyncTaskPool
from src.core.depends import _get_thread_pool, _get_async_task_pool

from src.auth.models import User
from src.auth.base_config import current_user

from src.web3.controllers.web3_controller import Web3Controller
from src.web3.domain.services.web3_service import Web3Service
from src.web3.gateways.moralis.moralis import MoralisClient

from src.binance_api.gateways.binance.binance_http import BinanceAPI
from src.binance_api.depends import _get_binance_api

from src.portfolio.domain.services.portfolio_service import PortfolioService
from src.portfolio.domain.services.operation_service import OperationService
from src.portfolio.depends import _get_portfolio_service, _get_operation_service


def _get_moralis_client():
    return MoralisClient()


def _get_web3_service(
        moralis_client: MoralisClient = Depends(_get_moralis_client),
        thread_pool: ThreadPool = Depends(_get_thread_pool),
        async_task_pool: AsyncTaskPool = Depends(_get_async_task_pool),
        binance_api: BinanceAPI = Depends(_get_binance_api)
) -> Web3Service:
    return Web3Service(
        moralis_client=moralis_client,
        thread_pool=thread_pool,
        async_task_pool=async_task_pool,
        binance_api=binance_api
    )


def get_web3_controller(
        user: User = Depends(current_user),
        web3_service: Web3Service = Depends(_get_web3_service),
        portfolio_service: PortfolioService = Depends(_get_portfolio_service),
        operation_service: OperationService = Depends(_get_operation_service)
) -> Web3Controller:
    return Web3Controller(
        user=user,
        web3_service=web3_service,
        portfolio_service=portfolio_service,
        operation_service=operation_service
    )

