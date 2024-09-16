from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends
from src.portfolio.controllers.operation_controller import OperationController
from src.portfolio.schemas.schema import OperationSchema, OperationCreateSchema
from starlette import status
from src.portfolio.depends import get_operation_controller

if TYPE_CHECKING:
    from src.portfolio.models.models import Operation


operation_router = APIRouter(
    prefix='/api/portfolio/operation',
    tags=['portfolio']
)


@operation_router.post(
    '/',
    response_model=OperationSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(
        new_operation: OperationCreateSchema,
        controller: OperationController = Depends(get_operation_controller),
) -> Operation:
    return await controller.create(new_operation=new_operation)


@operation_router.get(
    '/{portfolio_id}/',
    response_model=list[OperationSchema],
    status_code=status.HTTP_200_OK
)
async def list(
        portfolio_id: int,
        controller: OperationController = Depends(get_operation_controller),
) -> list[Operation]:
    return await controller.list(portfolio_id=portfolio_id)


@operation_router.delete(
    '/{operation_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        operation_id: int,
        controller: OperationController = Depends(get_operation_controller),
):
    await controller.delete(
        operation_id=operation_id
    )
