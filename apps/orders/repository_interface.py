from abc import ABC, abstractmethod
from apps.orders.entity import Order
from apps.products.product_entity import Product

class OrderRepositoryInterface(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order:
        pass

    # @abstractmethod
    # def reserve_stock(self, product: Product, remaining_quantity: int) -> bool:
    #     pass