from __future__ import annotations

from typing import TYPE_CHECKING

from src.portfolio.domain.repos.operation_change_command_repo import OperationChangeCommandRepo
from src.portfolio.domain.repos.operation_read_command_repo import OperationReadCommandRepo
from src.portfolio.domain.repos.portfolio_repo import PortfolioRepo
from src.core.exceptions import NotFoundPortfolioError, NotFoundOperationError, NotEnoughTokenOperationError
from src.portfolio.schemas.schema import OperationCreateSchema

if TYPE_CHECKING:
    from src.portfolio.models.models import Operation


class OperationService:
    def __init__(
            self,
            operation_read_command_repo: OperationReadCommandRepo,
            operation_change_command_repo: OperationChangeCommandRepo,
            portfolio_repo: PortfolioRepo
    ) -> None:
        self.operation_read_command_repo = operation_read_command_repo
        self.operation_change_command_repo = operation_change_command_repo
        self.portfolio_repo = portfolio_repo

    async def create(self, new_operation: OperationCreateSchema, user_id: int) -> Operation:
        if not await self.portfolio_repo.get_user_portfolio_by_id(
                portfolio_id=new_operation.portfolio_id,
                user_id=user_id
        ):
          raise NotFoundPortfolioError
        if not await self.operation_read_command_repo.check_diff_amount(
                portfolio_id=new_operation.portfolio_id,
                new_operation=new_operation
        ):
            raise NotEnoughTokenOperationError

        return await self.operation_change_command_repo.create(new_operation=new_operation)
    
    async def list(self, portfolio_id: int) -> list[Operation]:
        return await self.operation_read_command_repo.list_operation(portfolio_id=portfolio_id)

    async def bulk_create(self, operations: list[OperationCreateSchema], user_id: int) -> list[Operation]:
        if not await self.portfolio_repo.get_user_portfolio_by_id(
                portfolio_id=operations[0].portfolio_id,
                user_id=user_id
        ):
          raise NotFoundPortfolioError
        return await self.operation_change_command_repo.bulk_create(operations=operations)

    async def delete(self, user_id: int, operation_id: int) -> None:
        if not await self.operation_read_command_repo.get_operation_by_id(
                user_id=user_id,
                operation_id=operation_id
        ):
            raise NotFoundOperationError
        await self.operation_change_command_repo.delete(operation_id=operation_id)
