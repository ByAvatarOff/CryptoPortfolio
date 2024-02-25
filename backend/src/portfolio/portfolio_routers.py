from auth.base_config import current_user
from auth.models import User
from fastapi import APIRouter, Depends
from portfolio.portfolio_schemas import PortfolioCreateSchema, PortfolioSchema
from portfolio.portfolio_service import PortfolioService
from starlette import status

portfolio_router = APIRouter(
    prefix='/api/portfolio',
    tags=['portfolio']
)


@portfolio_router.get('/list_all_operation/',
                      response_model=list[PortfolioSchema],
                      status_code=status.HTTP_200_OK)
async def list_all_operation(
        user: User = Depends(current_user),
        portfolio_service: PortfolioService = Depends()
) -> list[PortfolioSchema]:
    """Return list all user operation in portfolio"""
    return await portfolio_service.list_operation(user_id=user.id)


@portfolio_router.post('/create_operation/',
                       response_model=list[PortfolioSchema],
                       status_code=status.HTTP_201_CREATED)
async def add_operation(
        new_operation: PortfolioCreateSchema,
        user: User = Depends(current_user),
        portfolio_service: PortfolioService = Depends(),
) -> list[PortfolioSchema]:
    """Create operation in portfolio"""
    return await portfolio_service.create_operation(
        user_id=user.id,
        new_operation=new_operation
    )


@portfolio_router.delete('/delete_operation/{operation_id}/',
                         response_model=list[PortfolioSchema],
                         status_code=status.HTTP_200_OK)
async def delete_operation(
        operation_id: int,
        user: User = Depends(current_user),
        portfolio_service: PortfolioService = Depends(),
) -> list[PortfolioSchema]:
    """Delete user operation in portfolio and return new list with operation"""
    return await portfolio_service.delete_operation(
        user_id=user.id,
        operation_id=operation_id
    )
