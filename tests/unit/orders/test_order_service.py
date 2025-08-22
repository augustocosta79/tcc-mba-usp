from datetime import datetime
from uuid import uuid4
from unittest.mock import MagicMock

import pytest
from apps.orders.service import OrderService
from apps.orders.enums import OrderStatus
from apps.orders.schemas import OrderSchema
from apps.orders.entity import OrderItem
from apps.shared.value_objects import Price, Stock
from apps.shared.exceptions import OutOfStockError


@pytest.fixture
def order_service():
    repository = MagicMock()
    user_service = MagicMock()
    cart_service = MagicMock()
    address_service = MagicMock()
    return OrderService(repository, user_service, cart_service, address_service)


def create_mock_product(id=None, price=100, stock=10, title="Test Product"):
    product = MagicMock()
    product.id = id or uuid4()
    product.price = Price(price)
    product.stock = Stock(stock)
    product.title.value = title
    product.description.value = f"Description for {title}"
    product.owner_id = uuid4()
    product.categories = []
    product.is_active = True
    product.created_at = datetime.now()
    product.updated_at = datetime.now()
    return product

def create_mock_user():
    user = MagicMock()
    user.id = uuid4()
    user.name.value = "Test User"
    user.email.value = "test@mail.com"
    user.username = "testUsername"
    user.is_active = True
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    return user

def create_mock_address(id=None, user_id=None):
    address = MagicMock()
    address.id = id or uuid4()
    address.user_id = user_id or uuid4()
    address.street.value = "Test Street"
    address.street_number.value = "123"
    address.complement.value = "Apt 101"
    address.district.value = "Test District"
    address.city.value = "Test City"
    address.state_code.value = "ST"
    address.postal_code.value = "12345678"
    address.country.value = "BR"
    address.is_default = True
    return address

def create_mock_cart_item(product=None, quantity=1):
    cart_item = MagicMock()
    cart_item.product = product or create_mock_product()
    cart_item.quantity = quantity
    return cart_item

def create_mock_cart(items=None):
    cart = MagicMock()
    cart.items = items or [create_mock_cart_item()]
    return cart

@pytest.mark.django_db # usado por causa do atomic apenas
class TestOrderCreation:
    def test_create_order_success(self, order_service):
        user_id = uuid4()
        address_id = uuid4()

        product1 = create_mock_product(price=100, stock=10)
        product2 = create_mock_product(price=200, stock=5)

        cart = create_mock_cart([
        create_mock_cart_item(product1, 2),
        create_mock_cart_item(product2, 1)
        ])
        order_service.cart_service.get_cart_by_user.return_value = cart

        address = create_mock_address(id=address_id, user_id=user_id)
        order_service.address_service.get_address_by_id.return_value = address

        user = create_mock_user()
        order_service.user_service.get_user_by_id.return_value = user

        order_service.repository.reserve_stock.return_value = True
        order_service.repository.save.side_effect = lambda order: order

        result = order_service.create_order(user_id, address_id)

        assert isinstance(result, OrderSchema)
        assert result.status == OrderStatus.PENDING
        assert len(result.items) == 2
        assert result.user.id == user.id
        assert result.address.id == address.id


    def test_create_order_out_of_stock(self, order_service):
        user_id = uuid4()
        address_id = uuid4()

        product = MagicMock()
        product.id = uuid4()
        product.price = Price(100)
        product.stock = Stock(1)  # Estoque insuficiente

        cart_item = MagicMock()
        cart_item.product = product
        cart_item.quantity = 5

        cart = MagicMock()
        cart.items = [cart_item]
        order_service.cart_service.get_cart_by_user.return_value = cart

        address = MagicMock()
        address.id = address_id
        order_service.address_service.get_address_by_id.return_value = address

        with pytest.raises(OutOfStockError):
            order_service.create_order(user_id, address_id)
