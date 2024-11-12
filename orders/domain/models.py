from pydantic import BaseModel


class OrderCreate(BaseModel):
    """
    Модель для создания заказа.

    Атрибуты:
        user_id (str): Идентификатор пользователя.
        item (str): Наименование товара.
        quantity (int): Количество.
    """

    user_id: str
    item: str
    quantity: int
