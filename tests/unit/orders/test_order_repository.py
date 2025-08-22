from uuid import uuid4
from apps.carts.repository import CartRepository
from apps.carts.entity import Cart, CartItem
from apps.carts.service import CartService
from apps.products.service import ProductService
from apps.products.repository import ProductRepository
from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from apps.products.product_entity import Product
from apps.orders.repository import OrderRepository
from apps.orders.entity import Order, OrderItem
from utils.logger import configure_logger
from apps.addresses.service import AddressService
from apps.addresses.repository import AddressRepository
from apps.orders.enums import OrderStatus
import pytest


test_logger = configure_logger("order_test_repository")
user_service = UserService(UserRepository(), test_logger)
product_service = ProductService(ProductRepository(), test_logger)
category_service = CategoryService(CategoryRepository(), test_logger)
cart_repository = CartRepository()
address_repository = AddressRepository()
address_service = AddressService(address_repository, test_logger)
cart_service = CartService(cart_repository, product_service, user_service, test_logger)

repository = OrderRepository()

@pytest.mark.django_db
class TestOrderRepository:
    def test_should_save_order_data_and_return_entity(self):
        user = user_service.create_user('test', 'teste@testmail.com', 'Abc@1234')
        category = category_service.create_category('categ', 'categ descript')
        address = address_service.create_address(user.id, 'rua humberto de campos', '382', '402', 'Leblon', 'Rio de janeiro', 'RJ', '22430190', 'BR', True)
        
        product1 = product_service.create_product('prod one', 'descrittion 1', 5, 10, user.id, [category.id])
        product2 = product_service.create_product('prod two', 'descrittion 2', 5, 10, user.id, [category.id])

        reserved_quantity_1 = 2
        reserved_quantity_2 = 3

        cart_service.add_to_cart(user.id, product1.id, reserved_quantity_1)
        cart = cart_service.add_to_cart(user.id, product2.id, reserved_quantity_2)

        order_items = [ OrderItem(item.product.id, item.quantity, item.product.price) for item in cart.items ]

        order = Order(user.id, address.id, order_items, OrderStatus.PENDING)

        saved_order = repository.save(order)

        assert saved_order.id == order.id
        assert len(saved_order.items) == 2
        assert len(saved_order.items) == len(order.items)
        assert saved_order.items[0].product_id == order.items[0].product_id
        assert saved_order.items[1].product_id == order.items[1].product_id
        assert saved_order.items[0].quantity == order.items[0].quantity
        assert saved_order.items[1].quantity == order.items[1].quantity
        assert saved_order.items[0].quantity == reserved_quantity_1
        assert saved_order.items[1].quantity == reserved_quantity_2