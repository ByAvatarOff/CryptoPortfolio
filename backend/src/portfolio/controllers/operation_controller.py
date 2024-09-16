from __future__ import annotations

from typing import TYPE_CHECKING

from src.auth.models import User
from src.portfolio.domain.services.operation_service import OperationService


if TYPE_CHECKING:
    from src.portfolio.models.models import Operation
    from src.portfolio.schemas.schema import OperationCreateSchema


class OperationController:
    def __init__(
            self,
            user: User,
            operation_service: OperationService
    ) -> None:
        self.user = user
        self.operation_service = operation_service

    async def create(self, new_operation: OperationCreateSchema) -> Operation:
        return await self.operation_service.create(
            new_operation=new_operation,
            user_id=self.user.id,
        )
    
    async def list(self, portfolio_id: int) -> list[Operation]:
        return await self.operation_service.list(portfolio_id=portfolio_id)

    async def delete(self, operation_id: int) -> None:
        await self.operation_service.delete(
            user_id=self.user.id,
            operation_id=operation_id
        )
