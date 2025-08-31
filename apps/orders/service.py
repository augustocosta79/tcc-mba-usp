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
from apps.shared.exceptions import NotFoundError
from utils.logger import configure_logger

logger = configure_logger(__name__)


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
        self.logger = logger

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
            saved_order = self.repository.save(order)
            
            products = [
                self.product_service.get_product_by_id(item.product_id)
                for item in saved_order.items
            ]


            return OrderDTO.build(saved_order, user, address, products)
        
    def get_order_by_id(self, order_id: UUID):
        order = self._get_order_or_raise(order_id)
        user = self.user_service.get_user_by_id(order.user_id)
        address = self.address_service.get_address_by_id(order.address_id)
        products = [ self.product_service.get_product_by_id(item.product_id) for item in order.items ]

        return OrderDTO.build(order, user, address, products)

    
    def list_orders_by_user_id(self, user_id: UUID):
        user = self.user_service.get_user_by_id(user_id)
        orders = self.repository.list_orders_by_user_id(user.id)

        return [
            OrderDTO.build(
                order,
                user,
                self.address_service.get_address_by_id(order.address_id),
                [ self.product_service.get_product_by_id(item.product_id) for item in order.items ]
            )
            for order in orders
        ]
    
    def set_status(self, order_id: UUID, new_status: OrderStatus):
        order = self._get_order_or_raise(order_id)
        order.set_status(new_status)
        self.repository.set_status(order.id, new_status)
        user = self.user_service.get_user_by_id(order.user_id)
        address = self.address_service.get_address_by_id(order.address_id)
        products = [ self.product_service.get_product_by_id(item.product_id) for item in order.items ]

        return OrderDTO.build(order, user, address, products)
    
    def remove_item_from_order(self, order_id: UUID, item_id: UUID):
        order = self._get_order_or_raise(order_id)

        with transaction.atomic():
            item = order.get_item(item_id)
            # 3. Liberar estoque
            self.product_service.release_stock(item.product_id, item.quantity)
            # 4. Atualizar entidade na memória
            order.remove_item(item_id)
            # 5. Remover item do banco
            self.repository.delete_order_item(item_id)
            # 6. Atualizar pedido no banco se necessário (ex: total)
            self.repository.update_order(order)
            
            user = self.user_service.get_user_by_id(order.user_id)
            address = self.address_service.get_address_by_id(order.address_id)
            products = [ self.product_service.get_product_by_id(item.product_id) for item in order.items ]
            return OrderDTO.build(order, user, address, products)
        
    def increase_order_item_quantity(self, order_id: UUID, item_id: UUID, quantity: int):
        order = self._get_order_or_raise(order_id)

        with transaction.atomic():
            item = order.get_item(item_id)
            self.product_service.reserve_stock(item.product_id, quantity)
            order.increase_item_quantity(item.id, quantity)
            self.repository.update_order(order)

            user = self.user_service.get_user_by_id(order.user_id)
            address = self.address_service.get_address_by_id(order.address_id)
            products = [ self.product_service.get_product_by_id(item.product_id) for item in order.items ]
            return OrderDTO.build(order, user, address, products)

    
    def cancel_order(self, order_id: UUID):
        order = self._get_order_or_raise(order_id)
        
        with transaction.atomic():
            order.cancel()
            for item in order.items:
                self.product_service.release_stock(item.product_id, item.quantity)
            self.repository.update_order(order)

            user = self.user_service.get_user_by_id(order.user_id)
            address = self.address_service.get_address_by_id(order.address_id)
            products = [ self.product_service.get_product_by_id(item.product_id) for item in order.items ]
            return OrderDTO.build(order, user, address, products)


    
    def _get_order_or_raise(self, order_id: UUID) -> Order:
        if not (order := self.repository.get_order_by_id(order_id)):
            raise NotFoundError("Order not found")
        return order 


    
