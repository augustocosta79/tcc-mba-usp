from typing import List, Optional
from uuid import UUID, uuid4

from apps.orders.enums import OrderStatus
from apps.shared.value_objects import Price


class OrderItem:
    def __init__(
        self, product_id: UUID, quantity: int, price: Price, id: Optional[UUID] = None
    ):
        self._product_id = product_id
        self._quantity = quantity
        self._price = price
        self._id = id or uuid4()

    @property
    def product_id(self):
        return self._product_id

    @property
    def quantity(self):
        return self._quantity

    @property
    def price(self):
        return self._price

    @property
    def id(self):
        return self._id


class Order:
    def __init__(
        self,
        user_id: UUID,
        address_id: UUID,
        items: List[OrderItem],
        status: OrderStatus,
        id: Optional[UUID] = None,
    ):
        self._user_id = user_id
        self._address_id = address_id
        self._items = items
        self._id = id or uuid4()
        self._status = status
        self._total_amount = sum((item.price for item in items), Price(0))

    @property
    def id(self):
        return self._id

    @property
    def address_id(self):
        return self._address_id

    @property
    def items(self):
        return self._items

    @property
    def status(self):
        return self._status

    @property
    def user_id(self):
        return self._user_id
    
    @property
    def total_amount(self) -> Price:
        return self._total_amount
