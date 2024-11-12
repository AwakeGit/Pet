import asyncio

from bson import ObjectId
from domain.models import OrderCreate
from fastapi import HTTPException
from infrastructure.db import db
from infrastructure.kafka_producer import send_order_created_event


async def create_order(order: OrderCreate):
    """
    Создать новый заказ и опубликовать событие в Kafka.

    Args:
        order (OrderCreate): Данные заказа.

    Returns:
        dict: Идентификатор созданного заказа.
    """
    await asyncio.sleep(10)
    order_doc = order.dict()
    result = await db.orders.insert_one(order_doc)
    order_id = str(result.inserted_id)
    event = {"order_id": order_id, **order_doc}
    await send_order_created_event(event)
    return {"order_id": order_id}


async def get_order(order_id: str):
    """
    Получить заказ по идентификатору.

    Args:
        order_id (str): Идентификатор заказа.

    Returns:
        dict: Данные заказа.

    Raises:
        HTTPException: Если заказ не найден или id некорректен.
    """
    try:
        obj_id = ObjectId(order_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid order_id format")
    order = await db.orders.find_one({"_id": obj_id})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["_id"] = str(order["_id"])
    return order
