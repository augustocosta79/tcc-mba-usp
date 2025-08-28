from abc import ABC, abstractmethod
from uuid import UUID
from apps.orders.entity import Order
from apps.orders.enums import OrderStatus


class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: UUID) -> Order:
        pass

    @abstractmethod
    def list_orders_by_user_id(self, user_id: UUID) -> list[Order]:
        pass

    @abstractmethod
    def set_status(self, order_id: UUID, new_status: OrderStatus) -> None:
        pass

    @abstractmethod
    def delete_order_item(self, item_id: UUID) -> None:
        pass

    @abstractmethod
    def update_order(self, order: Order) -> Order:
        pass