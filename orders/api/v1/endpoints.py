from application.commands import create_order, get_order
from domain.models import OrderCreate
from fastapi import APIRouter

router = APIRouter()


@router.post("/orders")
async def create_order_endpoint(order: OrderCreate):
    return await create_order(order)


@router.get("/orders/{order_id}")
async def get_order_endpoint(order_id: str):
    return await get_order(order_id)
