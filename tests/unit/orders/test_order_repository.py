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

def create_test_order(reserved_quantity_1, reserved_quantity_2):
    user = user_service.create_user('test', 'teste@testmail.com', 'Abc@1234')
    category = category_service.create_category('categ', 'categ descript')
    address = address_service.create_address(user.id, 'rua humberto de campos', '382', '402', 'Leblon', 'Rio de janeiro', 'RJ', '22430190', 'BR', True)
    
    product1 = product_service.create_product('prod one', 'descrittion 1', 5, 10, user.id, [category.id])
    product2 = product_service.create_product('prod two', 'descrittion 2', 5, 10, user.id, [category.id])

    

    cart_service.add_to_cart(user.id, product1.id, reserved_quantity_1)
    cart = cart_service.add_to_cart(user.id, product2.id, reserved_quantity_2)

    for item in cart.items:
        print(f"DEBUG: product_id={item.product.id}, price={item.product.price}, type={type(item.product.price)}")

    order_items = [ OrderItem(item.product.id, item.quantity, item.product.price) for item in cart.items ]

    return Order(user.id, address.id, order_items, OrderStatus.PENDING)

def assert_order_is_equal(original_order, saved_order, reserved_quantity_1, reserved_quantity_2):
    assert saved_order.id == original_order.id
    assert len(saved_order.items) == 2
    assert len(saved_order.items) == len(original_order.items)
    assert saved_order.items[0].id == original_order.items[0].id
    assert saved_order.items[0].product_id == original_order.items[0].product_id
    assert saved_order.items[1].product_id == original_order.items[1].product_id
    assert saved_order.items[0].quantity == original_order.items[0].quantity
    assert saved_order.items[1].quantity == original_order.items[1].quantity
    assert saved_order.items[0].quantity == reserved_quantity_1
    assert saved_order.items[1].quantity == reserved_quantity_2

@pytest.mark.django_db
class TestOrderRepository:
    def test_should_save_order_data_and_return_entity(self):
        reserved_quantity_1 = 2
        reserved_quantity_2 = 3
        
        order = create_test_order(reserved_quantity_1, reserved_quantity_2)

        saved_order = repository.save(order)

        assert_order_is_equal(order, saved_order, reserved_quantity_1, reserved_quantity_2)
        assert saved_order.status == OrderStatus.PENDING

        

    def test_should_get_order_by_id_successfully(self):
        reserved_quantity_1 = 2
        reserved_quantity_2 = 3
        
        order = create_test_order(reserved_quantity_1, reserved_quantity_2)

        saved_order = repository.save(order)

        retrieved_order = repository.get_order_by_id(saved_order.id)

        assert_order_is_equal(saved_order, retrieved_order, reserved_quantity_1, reserved_quantity_2)

    def test_should_list_orders_by_user_id(self):
        reserved_quantity_1 = 2
        reserved_quantity_2 = 3
        
        order = create_test_order(reserved_quantity_1, reserved_quantity_2)

        saved_order = repository.save(order)

        orders = repository.list_orders_by_user_id(saved_order.user_id)

        listed_order = orders[0]

        assert_order_is_equal(saved_order, listed_order, reserved_quantity_1, reserved_quantity_2)

    def test_should_change_order_status(self):
        reserved_quantity_1 = 2
        reserved_quantity_2 = 3
        
        order = create_test_order(reserved_quantity_1, reserved_quantity_2)
        saved_order = repository.save(order)

        order_approved = repository.set_status(saved_order.id, OrderStatus.APPROVED)
        assert_order_is_equal(order_approved, saved_order, reserved_quantity_1, reserved_quantity_2)
        assert order_approved.status == OrderStatus.APPROVED

    def test_should_update_order_successfully(self):
        reserved_quantity_1 = 2
        reserved_quantity_2 = 3
        
        # 1. Criar pedido inicial
        order = create_test_order(reserved_quantity_1, reserved_quantity_2)
        saved_order = repository.save(order)

        # 2. Criar novo endereço para atualizar o pedido
        new_address = address_service.create_address(
            saved_order.user_id,
            'rua das laranjeiras', '123', '501',
            'Laranjeiras', 'Rio de Janeiro', 'RJ',
            '22240003', 'BR', False
        )

        # 3. Alterar status, endereço e itens
        # saved_order._status = OrderStatus.SHIPPED
        saved_order._address_id = new_address.id
        saved_order._items.pop()  # remove um item
        saved_order._items[0]._quantity = 4  # altera quantidade do item restante

        # 4. Chamar update_order
        updated_order = repository.update_order(saved_order)

        # 5. Validar campos básicos
        assert updated_order.id == saved_order.id
        # assert updated_order.status == OrderStatus.SHIPPED
        assert updated_order.address_id == new_address.id
        assert updated_order.user_id == saved_order.user_id

        # 6. Validar itens
        assert len(updated_order.items) == 1
        assert updated_order.items[0].product_id == saved_order.items[0].product_id
        assert updated_order.items[0].quantity == 4

        # 7. Validar total_amount recalculado
        expected_total = updated_order.items[0].price.value * updated_order.items[0].quantity
        assert updated_order.total_amount.value == expected_total

        # 8. Validar que o get_order_by_id reflete as alterações
        retrieved_order = repository.get_order_by_id(updated_order.id)
        assert retrieved_order.address_id == new_address.id
        # assert retrieved_order.status == OrderStatus.SHIPPED
        assert len(retrieved_order.items) == 1
        assert retrieved_order.items[0].quantity == 4

    def test_should_delete_order_item_successfully(self):
        reserved_quantity_1 = 2
        reserved_quantity_2 = 3
        order = create_test_order(reserved_quantity_1, reserved_quantity_2)
        saved_order = repository.save(order)

        item_to_delete = saved_order.items[0]

        repository.delete_order_item(item_to_delete.id)

        updated_order = repository.get_order_by_id(saved_order.id)

        assert len(updated_order.items) == 1
        assert updated_order.items[0].id != item_to_delete.id
        assert updated_order.items[0].quantity == saved_order.items[1].quantity



