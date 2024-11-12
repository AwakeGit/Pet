import asyncio

from infrastructure.db import db
from infrastructure.kafka_consumer import consume_status_updates

active_connections = set()


async def handle_websocket(websocket):
    """
    Обработать подключение WebSocket для пользователя.

    Args:
        websocket (WebSocket): WebSocket-соединение клиента.
    """
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        active_connections.remove(websocket)


async def notify_on_status_update():
    """
    Запустить обработку событий Kafka и рассылку уведомлений по WebSocket.
    """

    async def handle_status_update(event):
        print(f"[DEBUG] Получено событие для уведомления: {event}")
        await db.notifications.insert_one(event)
        print(f"Уведомление сохранено: {event}")
        await asyncio.sleep(10)
        print(
            f"[NOTIFY] Пользователь {event.get('user_id')}: статус заказа {event.get('order_id')} "
            f"изменён на {event.get('status')}"
        )
        for ws in list(active_connections):
            try:
                await ws.send_json(event)
            except Exception:
                active_connections.remove(ws)

    loop = asyncio.get_event_loop()
    loop.create_task(consume_status_updates(handle_status_update))
