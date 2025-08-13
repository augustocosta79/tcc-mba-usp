from uuid import uuid4
from apps.carts.repository import CartRepository
from apps.carts.entity import Cart, CartItem
from apps.products.service import ProductService
from apps.products.repository import ProductRepository
from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from apps.products.product_entity import Product
from utils.logger import configure_logger
import pytest


test_logger = configure_logger("cart_test_repository")
user_service = UserService(UserRepository(), test_logger)
product_service = ProductService(ProductRepository(), test_logger)
category_service = CategoryService(CategoryRepository(), test_logger)


repository = CartRepository()

@pytest.mark.django_db
@pytest.fixture
def test_cart():
    user = user_service.create_user('test', 'test@test.com', 'Abc@1234')
    category = category_service.create_category('test cat', 'test cat desc')
    product = product_service.create_product('test', 'test description', '2.22', 1, user.id, [category.id])
    quantity = 1
    cart_item = CartItem(product, quantity)
    cart_id = uuid4()
    cart = Cart(user.id, [cart_item], cart_id)
    return cart


@pytest.mark.django_db
@pytest.fixture
def saved_cart(test_cart):
    saved_cart = repository.save(test_cart)
    return saved_cart

def assert_is_equal(saved_cart, cart):
    assert isinstance(saved_cart, Cart)
    assert saved_cart.id == cart.id
    assert saved_cart.user_id == cart.user_id
    assert isinstance(saved_cart.items, list)
    assert len(saved_cart.items) == 1
    assert isinstance(saved_cart.items[0], CartItem)
    assert isinstance(saved_cart.items[0].product, Product)
    assert saved_cart.items[0].product.id == cart.items[0].product.id
    assert saved_cart.items[0].quantity == cart.items[0].quantity


@pytest.mark.django_db
class TestCartRepository:
    def test_should_save_cart_data_and_return_entity_successfully(self, test_cart, saved_cart: Cart):
        assert_is_equal(saved_cart, test_cart)

    def test_should_get_cart_by_user_id_successfully(self, saved_cart: Cart):
        retrieved_cart = repository.get_cart_by_user(saved_cart.user_id)
        assert_is_equal(saved_cart, retrieved_cart)

    def test_should_update_cart_data_and_return_entity_successfully(self, saved_cart: Cart):
        user = user_service.create_user('test two', 'test2@test.com', 'Abc@1234')
        category = category_service.create_category('test cat', 'test2 cat desc')
        product = product_service.create_product('test2', 'test2 description', '2.22', 1, user.id, [category.id])
        quantity = 1
        new_cart_item = CartItem(product, quantity)

        assert len(saved_cart.items) == 1
        saved_cart.items.append(new_cart_item)

        updated_cart = repository.update(saved_cart)
        assert len(updated_cart.items) == 2

        added_item = updated_cart.items[1]
        assert added_item.product.id == new_cart_item.product.id
        assert added_item.quantity == new_cart_item.quantity

        saved_cart.items.clear()
        updated_cart = repository.update(saved_cart)
        assert len(updated_cart.items) == 0