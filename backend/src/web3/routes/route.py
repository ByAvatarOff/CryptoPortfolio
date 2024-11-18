from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, UploadFile, File, Form
from src.web3.schemas.schema import Web3Addresses
from starlette import status
from src.web3.depends import get_web3_controller
from src.portfolio.schemas.schema import PortfolioSchema

if TYPE_CHECKING:
    from src.web3.controllers.web3_controller import Web3Controller


web3_router = APIRouter(
    prefix='/api/web3',
    tags=['web3']
)

@web3_router.post(
    "/create_portfolio/",
    response_model=PortfolioSchema,
    status_code=status.HTTP_200_OK
)
async def create_web3_portfolio(
        web3_data: list = Form(...),
        name: str = Form(...),
        image: UploadFile = File(...),
        controller: Web3Controller = Depends(get_web3_controller),
):
    return await controller.create_web3_portfolio(name=name, image=image, web3_data=web3_data)
