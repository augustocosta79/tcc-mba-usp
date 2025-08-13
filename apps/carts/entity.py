from typing import Optional
from uuid import UUID, uuid4
from apps.products.product_entity import Product
from apps.shared.exceptions import NotFoundError, ConflictError

class CartItem:
    def __init__(self, product: Product, quantity: int, id: Optional[UUID]=None):
        self._product = product
        self._quantity = quantity
        self._id = id or uuid4()
        
    @property
    def product(self) -> Product:
        return self._product
    
    @property
    def quantity(self) -> int:
        return self._quantity
    
    @property
    def id(self):
        return self._id



class Cart:
    def __init__(self, user_id: UUID, items: Optional[list[CartItem]]=None, id: Optional[UUID]=None):
        self._user_id = user_id
        self._items = items or []
        self._id = id or uuid4()

    @property
    def id(self):
        return self._id

    @property
    def user_id(self) -> UUID:
        return self._user_id
    
    @property
    def items(self) -> list[CartItem]:
        return self._items

    def add_item(self, cart_item: CartItem):
        for item in self._items:
            if item.product.id == cart_item.product.id:
                item.quantity += cart_item.quantity
                return
        self._items.append(cart_item)

    def subtract_item_quantity(self, product_id: UUID, quantity: int):
        for item in self.items:
            if item.product.id == product_id:
                if item._quantity - quantity < 0:
                    raise ConflictError("Quantity cannot be negative")
                item._quantity -= quantity
                return
        raise NotFoundError(f"Product {product_id} not found in cart")

