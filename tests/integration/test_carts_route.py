import json

import pytest
from apps.carts.entity import Cart, CartItem
from apps.carts.repository import CartRepository
from apps.categories.repository import CategoryRepository
from apps.categories.service import CategoryService
from apps.products.repository import ProductRepository
from apps.products.service import ProductService
from apps.users.repository import UserRepository
from apps.users.service import UserService
from tests.utils.timed_client import TimedClient
from utils.logger import configure_logger

logger = configure_logger("test_cart_route")

cart_repository = CartRepository()

@pytest.fixture
def timed_client(client):
    return TimedClient(client)

@pytest.fixture
def user():
    user_service = UserService(UserRepository(), logger)
    return user_service.create_user('test user', 'test@test.com', 'Abc@1234', 'testusername')

@pytest.fixture
def category():
    return CategoryService(CategoryRepository(), logger).create_category('cat test', 'testing category')

@pytest.fixture
def product(user, category):
    product_service = ProductService(ProductRepository(), logger)
    return product_service.create_product('title', 'descripton', '2.99', 5, user.id, [category.id])


@pytest.mark.django_db
class TestAddToCartRoute:
    def test_should_add_new_cart_item_sucessfully(self, timed_client, user, category, product):
        url = f"/api/carts/{user.id}/add"

        payload = {
            "product_id": str(product.id),
            "quantity": 1
        }

        assert cart_repository.get_cart_by_user(user.id) is None

        response = timed_client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        assert cart_repository.get_cart_by_user(user.id) is not None

        body = response.json()

        assert body["items"][0]["product"]["id"] == payload["product_id"]
        assert body["items"][0]["product"]["title"] == str(product.title.value)
        assert body["items"][0]["product"]["description"] == str(product.description.value)
        assert body["items"][0]["product"]["price"] == str(product.price.value)
        assert body["items"][0]["product"]["stock"] == int(product.stock.value)
        assert body["items"][0]["product"]["owner_id"] == str(product.owner_id)
        assert body["items"][0]["product"]["categories"][0]["id"] == str(category.id)
        assert body["items"][0]["quantity"] == payload["quantity"]

        
@pytest.mark.django_db
class TestSubtractItemCartQuantityRoute:
    def test_should_subtract_valid_quantity_from_item_cart_successfully(self, timed_client, user, product):
        cart_item = CartItem(product, 3)
        cart = Cart(user.id, [cart_item])
        cart_repository.save(cart)
        
        url = f"/api/carts/{user.id}/subtract"

        payload = {
            "product_id": str(product.id),
            "quantity": 1
        }

        response = timed_client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200

        body = response.json()

        item = body["items"][0]
        assert item["product"]["id"] == str(product.id)
        assert item["quantity"] > 0
        assert cart_item.quantity - payload["quantity"] == item["quantity"]

