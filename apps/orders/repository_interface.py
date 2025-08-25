from abc import ABC, abstractmethod
from uuid import UUID
from apps.orders.entity import Order
from apps.products.product_entity import Product

class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: UUID):
        pass