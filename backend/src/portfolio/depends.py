from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.portfolio.controllers.portfolio_controller import PortfolioController
from src.portfolio.controllers.operation_controller import OperationController
from src.portfolio.domain.services.portfolio_service import PortfolioService
from src.portfolio.domain.services.operation_service import OperationService
from src.portfolio.domain.repos.portfolio_repo import PortfolioRepo
from src.portfolio.domain.repos.operation_change_command_repo import OperationChangeCommandRepo
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.core.database import get_async_session
from src.auth.models import User
from src.auth.base_config import current_user


def _get_portfolio_repo(session: AsyncSession = Depends(get_async_session)) -> PortfolioRepo:
    return PortfolioRepo(session=session)


def _get_portfolio_service(
        repo: PortfolioRepo = Depends(_get_portfolio_repo),
) -> PortfolioService:
    return PortfolioService(portfolio_repo=repo)


def get_portfolio_controller(
        user: User = Depends(current_user),
        service: PortfolioService = Depends(_get_portfolio_service),
) -> PortfolioController:
    return PortfolioController(
        user=user,
        portfolio_service=service
    )


def _get_operation_read_command_repo(
        session: AsyncSession = Depends(get_async_session)
) -> OperationReadCommandRepo:
    return OperationReadCommandRepo(session=session)

def _get_operation_change_command_repo(
        session: AsyncSession = Depends(get_async_session)
) -> OperationChangeCommandRepo:
    return OperationChangeCommandRepo(session=session)


def _get_operation_service(
        operation_change_command_repo: OperationChangeCommandRepo = Depends(_get_operation_change_command_repo),
        operation_read_command_repo: OperationReadCommandRepo = Depends(_get_operation_read_command_repo),
        portfolio_repo: PortfolioRepo = Depends(_get_portfolio_repo),
) -> OperationService:
    return OperationService(
        operation_change_command_repo=operation_change_command_repo,
        operation_read_command_repo=operation_read_command_repo,
        portfolio_repo=portfolio_repo
    )


def get_operation_controller(
        user: User = Depends(current_user),
        service: OperationService = Depends(_get_operation_service),
) -> OperationController:
    return OperationController(
        user=user,
        operation_service=service
    )
