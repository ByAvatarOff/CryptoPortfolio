from fastapi import Depends

from portfolio.portfolio_repo import PortfolioRepo
from portfolio.portfolio_schemas import PortfolioSchema, PortfolioCreateSchema
from portfolio.portfolio_utils import PortfolioSchemaConverter


class PortfolioService:
    """Portfolio Service"""
    def __init__(
            self,
            portfolio_repo: PortfolioRepo = Depends()
    ) -> None:
        self.portfolio_repo = portfolio_repo

    async def list_operation(
            self,
            user_id: int
    ) -> list[PortfolioSchema]:
        """Get list operations"""
        return await PortfolioSchemaConverter.convert_list_sequence_to_list_schema(
            await self.portfolio_repo.list_operation(user_id=user_id)
        )

    async def create_operation(
            self,
            user_id: int,
            new_operation: PortfolioCreateSchema
    ) -> list[PortfolioSchema]:
        """Create new operation and return new operations list"""
        return await PortfolioSchemaConverter.convert_list_sequence_to_list_schema(
            await self.portfolio_repo.create_operation(user_id=user_id, new_operation=new_operation)
        )

    async def delete_operation(
            self,
            user_id: int,
            operation_id: int
    ) -> list[PortfolioSchema]:
        """Delete operation"""
        return await PortfolioSchemaConverter.convert_list_sequence_to_list_schema(
            await self.portfolio_repo.delete_operation(user_id=user_id, operation_id=operation_id)
        )
