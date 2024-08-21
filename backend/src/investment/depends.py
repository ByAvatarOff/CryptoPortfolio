from fastapi import Depends

from src.investment.controllers.controller import InvestmentController
from src.investment.domain.services.service import InvestmentService
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.portfolio.depends import _get_operation_read_command_repo
from src.auth.models import User
from src.auth.base_config import current_user
from src.binance_api.gateways.binance.binance_http import BinanceAPI
from src.binance_api.depends import _get_binance_api


def _get_investment_service(
        repo: OperationReadCommandRepo = Depends(_get_operation_read_command_repo),
        binance_api: BinanceAPI = Depends(_get_binance_api),
) -> InvestmentService:
    return InvestmentService(
        operation_read_command_repo=repo,
        binance_api=binance_api
    )


def get_investment_controller(
        user: User = Depends(current_user),
        service: InvestmentService = Depends(_get_investment_service),
) -> InvestmentController:
    return InvestmentController(
        user=user,
        investment_service=service
    )