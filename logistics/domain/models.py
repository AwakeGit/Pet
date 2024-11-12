from pydantic import BaseModel


class StatusUpdate(BaseModel):
    """
    Модель для обновления статуса заказа.

    Атрибуты:
        order_id (str): Идентификатор заказа.
        status (str): Новый статус заказа.
    """

    order_id: str
    status: str
