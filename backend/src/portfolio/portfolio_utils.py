from typing import Sequence

from portfolio.portfolio_schemas import PortfolioSchema
from sqlalchemy import Row


class PortfolioSchemaConverter:
    """Portfolio schema converter"""
    @staticmethod
    async def convert_list_sequence_to_list_schema(
            list_operation: Sequence[Row]
    ) -> list[PortfolioSchema]:
        """convert list sequence row to list PortfolioSchema"""
        return [
            PortfolioSchema.model_validate(operation)
            for operation in list_operation
        ]
