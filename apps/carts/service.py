from uuid import UUID
from apps.carts.repository_interface import CartRepositoryInterface
from apps.products.service import ProductService
from apps.users.service import UserService
from apps.carts.entity import Cart
from apps.carts.entity import CartItem
from apps.shared.exceptions import NotFoundError
from logging import Logger

class CartService:
    def __init__(self, repository: CartRepositoryInterface, product_service: ProductService, user_service: UserService, logger: Logger):
        self.repository = repository
        self.product_service = product_service
        self.user_service = user_service
        self.logger = logger


    def create_cart(self, user_id) -> Cart:
        cart = self.repository.save(Cart(user_id))
        self.logger.info(f"Cart successfully created for user {user_id}")
        return cart
    
    def add_to_cart(self, user_id: UUID, product_id: UUID, quantity: int) -> Cart:
        user = self.user_service.get_user_by_id(user_id)
        cart = self.repository.get_cart_by_user(user.id)
        if not cart:
            cart = self.create_cart(user_id)        
        product = self.product_service.get_product_by_id(product_id)
        cart_item = CartItem(product, quantity)
        cart.add_item(cart_item)
        self.repository.update(cart)
        return cart
    
    def subtract_quantity_from_cart_item(self, user_id: UUID, product_id: UUID, quantity: int) -> Cart:
        cart = self.repository.get_cart_by_user(user_id)
        if not cart:
            raise NotFoundError(f"Cart not found for user id {user_id}")
        cart.subtract_item_quantity(product_id, quantity)
        self.repository.update(cart)
        return cart
    
    def remove_cart_item(self, user_id: UUID, product_id: UUID) -> Cart:
        cart = self.repository.get_cart_by_user(user_id)
        if not cart:
             raise NotFoundError(f"Cart not found for user id {user_id}")
        cart.remove_cart_item(product_id)
        self.repository.update(cart)
        return cart
    
    def clear_cart(self, user_id: UUID):
        cart = self.repository.get_cart_by_user(user_id)
        if not cart:
            raise NotFoundError(f"Cart not found for user id {user_id}")
        cart.clear_cart()
        self.repository.update(cart)
        return cart
    
    def get_cart_by_user(self, user_id: UUID):
        try:
            user = self.user_service.get_user_by_id(user_id)
        except NotFoundError as exc:
            raise NotFoundError(str(exc))
        
        cart = self.repository.get_cart_by_user(user.id)
        if not cart:
            raise NotFoundError(f"Cart not found for user {user_id}")
        return cart