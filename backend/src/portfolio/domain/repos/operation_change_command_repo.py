from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import delete, insert

from src.portfolio.models.models import Operation
from src.portfolio.schemas.schema import OperationCreateSchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class OperationChangeCommandRepo:
    def __init__(
            self,
            session: AsyncSession
    ) -> None:
        self.session = session
        self.model: type[Operation] = Operation

    async def create(
            self,
            new_operation: OperationCreateSchema
    ) -> Operation:
        stmt = insert(self.model).values(new_operation.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalar()

    async def bulk_create(
            self,
            operations: list[OperationCreateSchema]
    ) -> list[Operation]:
        operations_to_insert = [operation.model_dump() for operation in operations]
        result = await self.session.execute(insert(self.model).returning(self.model), operations_to_insert)
        await self.session.commit()
        return result.scalars().all()

    async def delete(self, operation_id: int) -> None:
        stmt = delete(Operation).where(self.model.id == operation_id)
        await self.session.execute(stmt)
        await self.session.commit()
