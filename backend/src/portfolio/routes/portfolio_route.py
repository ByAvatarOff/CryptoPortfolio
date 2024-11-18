from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from src.portfolio.schemas.schema import PortfolioSchema
from starlette import status
from src.portfolio.depends import get_portfolio_controller
from src.core.settings import settings

if TYPE_CHECKING:
    from src.portfolio.models.models import Portfolio
    from src.portfolio.controllers.portfolio_controller import PortfolioController


portfolio_router = APIRouter(
    prefix='/api/portfolio',
    tags=['portfolio']
)


@portfolio_router.post(
    '/',
    response_model=PortfolioSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(
        name: str = Form(...),
        image: UploadFile = File(...),
        controller: PortfolioController = Depends(get_portfolio_controller),
) -> Portfolio:
    if image.content_type not in settings.app.allow_upload_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type")
    return await controller.create(name=name, image=image)


@portfolio_router.get(
    '/',
    response_model=list[PortfolioSchema],
    status_code=status.HTTP_200_OK
)
async def list(
        controller: PortfolioController = Depends(get_portfolio_controller),
) -> list[Portfolio]:
    return await controller.list()


@portfolio_router.delete(
    '/{portfolio_id}/',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
        portfolio_id: int,
        controller: PortfolioController = Depends(get_portfolio_controller),
):
    await controller.delete(
        portfolio_id=portfolio_id
    )
