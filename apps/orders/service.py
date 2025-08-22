from uuid import UUID

from apps.addresses.service import AddressService
from apps.carts.service import CartService
from apps.orders.entity import Order, OrderItem
from apps.orders.enums import OrderStatus
from apps.orders.repository_interface import OrderRepositoryInterface
from apps.users.service import UserService
from apps.products.service import ProductService
from django.db import transaction
from apps.orders.dto import OrderDTO
from apps.orders.schemas import OrderSchema


class OrderService:
    def __init__(
        self,
        repository: OrderRepositoryInterface,
        user_service: UserService,
        product_service: ProductService,
        cart_service: CartService,
        address_service: AddressService,
    ):
        self.user_service = user_service
        self.product_service = product_service
        self.cart_service = cart_service
        self.address_service = address_service
        self.repository = repository

    def create_order(self, user_id: UUID, address_id: UUID) -> OrderSchema:
        cart = self.cart_service.get_cart_by_user(user_id)
        address = self.address_service.get_address_by_id(address_id)
        user = self.user_service.get_user_by_id(user_id)
        with transaction.atomic():
            order_items = []
            for item in cart.items:
                self.product_service.reserve_stock(item.product.id, item.quantity)
                order_items.append(
                    OrderItem(item.product.id, item.quantity, item.product.price)
                )

            order = Order(user_id, address.id, order_items, OrderStatus.PENDING)
            self.repository.save(order)
            
            products = [item.product for item in cart.items]


            return OrderDTO.build(order, user, address, products)
