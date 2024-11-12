from domain.services import handle_websocket
from infrastructure.db import db


async def get_history(user_id: str):
    """
    Получить историю уведомлений пользователя.

    Args:
        user_id (str): Идентификатор пользователя.

    Returns:
        list: Список уведомлений пользователя.
    """
    notifications = await db.notifications.find({"user_id": user_id}).to_list(100)
    return notifications


async def websocket_endpoint(websocket):
    """
    Обработать WebSocket-соединение для real-time уведомлений.

    Args:
        websocket (WebSocket): WebSocket-соединение клиента.
    """
    await handle_websocket(websocket)
