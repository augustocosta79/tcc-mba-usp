from typing import List, Optional
from uuid import UUID, uuid4

from apps.orders.enums import OrderStatus
from apps.shared.value_objects import Price
from apps.shared.exceptions import ConflictError, NotFoundError


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
        self._total_amount = self._calculate_total_amount()

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
    
    
    def set_status(self, new_status: OrderStatus):
        if self._status == new_status.previous:
            self._status = new_status
            return
        raise ConflictError(f"Can't change {self._status} order to {new_status}. It should be {new_status.previous}")
    
    def get_item(self, item_id: UUID) -> OrderItem:
        for item in self._items:
            if item.id == item_id:
                return item
        raise NotFoundError(f"OrderItem not found - ID {item_id}")
    
    def remove_item(self, item_id: UUID):
        item_to_remove = self.get_item(item_id)
        self._items.remove(item_to_remove)
        self._total_amount = self._calculate_total_amount()

    def _calculate_total_amount(self) -> None:
       return Price(sum(item.price.value * item.quantity for item in self._items))
    
    def cancel(self):
        allowed_current_status = [ OrderStatus.PENDING, OrderStatus.APPROVED ]
        if self._status not in allowed_current_status:
            raise ConflictError(f"Just {', '.join([ order_status.value for order_status in allowed_current_status])} orders can be canceled")
        self._status = OrderStatus.CANCELED

        
