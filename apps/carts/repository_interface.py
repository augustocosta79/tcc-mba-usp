from abc import ABC, abstractmethod
from uuid import UUID
from apps.carts.entity import Cart

class CartRepositoryInterface(ABC):
    @abstractmethod
    def save(self, cart: Cart) -> Cart:
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def get_cart_by_user(self, user_id: UUID) -> Cart:
        pass