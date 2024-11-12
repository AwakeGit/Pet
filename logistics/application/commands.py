import asyncio

from bson import ObjectId
from domain.models import StatusUpdate
from infrastructure.db import db, orders_db
from infrastructure.kafka_producer import send_status_changed_event


async def update_status(update: StatusUpdate):
    """
    Обновить статус заказа, сохранить в БД и опубликовать событие в Kafka.

    Args:
        update (StatusUpdate): Данные для обновления статуса.

    Returns:
        dict: Сообщение об успешном обновлении статуса.
    """
    await asyncio.sleep(10)
    try:
        obj_id = ObjectId(update.order_id)
    except Exception:
        obj_id = update.order_id
    order = await orders_db.orders.find_one({"_id": obj_id})
    user_id = order["user_id"] if order and "user_id" in order else None
    status_doc = update.dict()
    status_doc["user_id"] = user_id
    await db.statuses.insert_one(status_doc)
    await send_status_changed_event(status_doc)
    return {"message": "Status updated"}
