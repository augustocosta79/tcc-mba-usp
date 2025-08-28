from datetime import datetime
from uuid import uuid4
from unittest.mock import MagicMock, call

import pytest
from apps.orders.service import OrderService
from apps.orders.entity import Order
from apps.orders.enums import OrderStatus
from apps.orders.schemas import OrderSchema
from apps.shared.value_objects import Price, Stock
from apps.shared.exceptions import OutOfStockError


@pytest.fixture
def order_service():
    repository = MagicMock()
    user_service = MagicMock()
    product_service = MagicMock()
    cart_service = MagicMock()
    address_service = MagicMock()
    return OrderService(repository, user_service, product_service, cart_service, address_service)


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


def assert_order_is_equal(order, test_order, test_order_item):
    assert order.id == test_order.id
    assert order.user.id == test_order.user_id
    assert order.address.id == test_order.address_id
    assert len(order.items) == len(test_order.items)

    assert order.items[0].id == test_order_item.id
    assert order.items[0].product.id == test_order_item.product_id
    assert order.items[0].quantity == test_order_item.quantity
    assert order.items[0].price == str(test_order_item.price.value)

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

        mock_order_item1 = MagicMock()
        mock_order_item1.id = uuid4()
        mock_order_item1.product_id = product1.id
        mock_order_item1.quantity = 4
        mock_order_item1.price = product1.price

        mock_order_item2 = MagicMock()
        mock_order_item2.id = uuid4()
        mock_order_item2.product_id = product2.id
        mock_order_item2.quantity = 3
        mock_order_item2.price = product2.price
        
        mock_order = MagicMock()
        mock_order.id = uuid4()
        mock_order.user_id = user.id
        mock_order.address_id = address.id
        mock_order.items = [ mock_order_item1, mock_order_item2 ]
        mock_order.status = OrderStatus.PENDING

        order_service.repository.save.return_value = mock_order
        order_service.product_service.get_product_by_id.side_effect = [product1, product2]

        result = order_service.create_order(user_id, address_id)

        assert isinstance(result, OrderSchema)
        assert result.status == OrderStatus.PENDING
        assert len(result.items) == 2
        assert result.user.id == user.id
        assert result.address.id == address.id


    def test_should_fail_create_order_with_out_of_stock_product(self, order_service):
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

        user = create_mock_user()
        user.id = user_id
        order_service.user_service.get_user_by_id.return_value = user

        order_service.product_service.reserve_stock.side_effect = OutOfStockError("Out of stock product")

        with pytest.raises(OutOfStockError):
            order_service.create_order(user_id, address_id)

class TestGetOrderById:
    def test_should_get_order_by_id_successfully(self, order_service):
        mock_user = create_mock_user()
        mock_product = create_mock_product()
        mock_address = create_mock_address()
        
        mock_order_item = MagicMock()
        mock_order_item.id = uuid4()
        mock_order_item.product_id = mock_product.id
        mock_order_item.quantity = 4
        mock_order_item.price = mock_product.price
        
        mock_order = MagicMock()
        mock_order.id = uuid4()
        mock_order.user_id = mock_user.id
        mock_order.address_id = mock_address.id
        mock_order.items = [ mock_order_item ]
        mock_order.status = OrderStatus.PENDING


        order_service.repository.get_order_by_id.return_value = mock_order
        order_service.user_service.get_user_by_id.return_value = mock_user
        order_service.address_service.get_address_by_id.return_value = mock_address
        order_service.product_service.get_product_by_id.return_value = mock_product

        order = order_service.get_order_by_id(mock_order.id)

        order_service.repository.get_order_by_id.assert_called_once_with(mock_order.id)
        order_service.user_service.get_user_by_id.assert_called_once_with(mock_order.user_id)
        order_service.address_service.get_address_by_id.assert_called_once_with(mock_order.address_id)
        order_service.product_service.get_product_by_id.assert_called_once_with(mock_order_item.product_id)
        assert_order_is_equal(order, mock_order, mock_order_item)
        assert order.status == OrderStatus.PENDING

        


class TestUserOrderListing:
    def test_should_get_user_orders_list_successfully(self, order_service):
        mock_user = create_mock_user()
        mock_product = create_mock_product()
        mock_address = create_mock_address()

        mock_order_item = MagicMock()
        mock_order_item.id = uuid4()
        mock_order_item.product_id = mock_product.id
        mock_order_item.quantity = 4
        mock_order_item.price = mock_product.price
        
        mock_order = MagicMock()
        mock_order.id = uuid4()
        mock_order.user_id = mock_user.id
        mock_order.address_id = mock_address.id
        mock_order.items = [ mock_order_item ]
        mock_order.status = OrderStatus.PENDING

        order_service.repository.list_orders_by_user_id.return_value = [ mock_order ]
        order_service.user_service.get_user_by_id.return_value = mock_user
        order_service.address_service.get_address_by_id.return_value = mock_address
        order_service.product_service.get_product_by_id.return_value = mock_product

        orders = order_service.list_orders_by_user_id(mock_user.id)
        order_service.user_service.get_user_by_id(mock_user.id)
        order_service.repository.list_orders_by_user_id.assert_called_once_with(mock_user.id)
        order_service.address_service.get_address_by_id.assert_called_once_with(mock_address.id)
        order_service.product_service.get_product_by_id.assert_called_once_with(mock_order_item.product_id)
        assert isinstance(orders, list)
        assert len(orders) == 1
        order = orders[0]
        assert_order_is_equal(order, mock_order, mock_order_item)
        assert order.status == OrderStatus.PENDING


class TestOrderStatusChange:
    def test_should_change_order_status_successfully(self, order_service):
        mock_user = create_mock_user()
        mock_product = create_mock_product()
        mock_address = create_mock_address()

        mock_order_item = MagicMock()
        mock_order_item.id = uuid4()
        mock_order_item.product_id = mock_product.id
        mock_order_item.quantity = 4
        mock_order_item.price = mock_product.price
        
        order = Order(
            mock_user.id,
            mock_address.id,
            [mock_order_item],
            OrderStatus.PENDING
        )

        order_service.repository.get_order_by_id.return_value = order
        order_service.user_service.get_user_by_id.return_value = mock_user
        order_service.address_service.get_address_by_id.return_value = mock_address
        order_service.product_service.get_product_by_id.return_value = mock_product
        
        order_approved = order_service.set_status(order.id, OrderStatus.APPROVED)
        assert_order_is_equal(order_approved, order, mock_order_item)
        assert order_approved.status == OrderStatus.APPROVED
        
        order_shipped = order_service.set_status(order.id, OrderStatus.SHIPPED)
        assert order_shipped.status == OrderStatus.SHIPPED
        
        order_delivered = order_service.set_status(order.id, OrderStatus.DELIVERED)
        assert order_delivered.status == OrderStatus.DELIVERED


class TestRemoveItemFromOrder:
    @pytest.mark.django_db  # necessário pelo atomic
    def test_should_remove_item_from_order_successfully(self, order_service):
        mock_user = create_mock_user()
        mock_product1 = create_mock_product(price=100, stock=10)
        mock_product2 = create_mock_product(price=200, stock=5)
        mock_address = create_mock_address()

        mock_order_item1 = MagicMock()
        mock_order_item1.id = uuid4()
        mock_order_item1.product_id = mock_product1.id
        mock_order_item1.quantity = 2
        mock_order_item1.price = mock_product1.price

        mock_order_item2 = MagicMock()
        mock_order_item2.id = uuid4()
        mock_order_item2.product_id = mock_product2.id
        mock_order_item2.quantity = 1
        mock_order_item2.price = mock_product2.price

        order = Order(
            mock_user.id,
            mock_address.id,
            [mock_order_item1, mock_order_item2],
            OrderStatus.PENDING
        )

        # Mocks do serviço e repositório
        order_service.repository.get_order_by_id.return_value = order
        order_service.product_service.release_stock.return_value = True
        order_service.repository.delete_order_item.return_value = None
        order_service.repository.update_order.return_value = order


        # Mock do get_user_by_id, get_address_by_id e get_product_by_id
        order_service.user_service.get_user_by_id.return_value = mock_user
        order_service.address_service.get_address_by_id.return_value = mock_address

        order_service.product_service.get_product_by_id.return_value = mock_product2

        # Executar o método
        result_dto = order_service.remove_item_from_order(order.id, mock_order_item1.id)

        # Asserts principais
        order_service.repository.get_order_by_id.assert_called_once_with(order.id)
        order_service.product_service.release_stock.assert_called_once_with(
            mock_order_item1.product_id, mock_order_item1.quantity
        )
        order_service.repository.delete_order_item.assert_called_once_with(mock_order_item1.id)
        order_service.repository.update_order.assert_called_once_with(order)

        # Validar que o item foi removido da lista
        assert len(order.items) == 1
        assert order.items[0].id == mock_order_item2.id

        # Validar DTO retornado (somente o item restante)
        assert len(result_dto.items) == 1
        assert result_dto.items[0].id == mock_order_item2.id
        assert result_dto.items[0].product.id == mock_product2.id


class TestCancelOrder:
    @pytest.mark.django_db  # necessário pelo atomic
    def test_should_change_order_status_to_canceled_and_release_product_stock_successfully(self, order_service):
        mock_user = create_mock_user()
        mock_product1 = create_mock_product(price=100, stock=10)
        mock_product2 = create_mock_product(price=200, stock=5)
        mock_address = create_mock_address()

        mock_order_item1 = MagicMock()
        mock_order_item1.id = uuid4()
        mock_order_item1.product_id = mock_product1.id
        mock_order_item1.quantity = 2
        mock_order_item1.price = mock_product1.price

        mock_order_item2 = MagicMock()
        mock_order_item2.id = uuid4()
        mock_order_item2.product_id = mock_product2.id
        mock_order_item2.quantity = 1
        mock_order_item2.price = mock_product2.price

        order = Order(
            mock_user.id,
            mock_address.id,
            [mock_order_item1, mock_order_item2],
            OrderStatus.PENDING
        )

        # Mocks do serviço e repositório
        order_service.repository.get_order_by_id.return_value = order
        order_service.product_service.release_stock.return_value = True
        order_service.repository.update_order.return_value = order


        # Mock do get_user_by_id, get_address_by_id e get_product_by_id
        order_service.user_service.get_user_by_id.return_value = mock_user
        order_service.address_service.get_address_by_id.return_value = mock_address

        order_service.product_service.get_product_by_id.side_effect = [mock_product1, mock_product2]

        # Executar o método
        result_dto = order_service.cancel_order(order.id)

        # Asserts principais
        order_service.repository.get_order_by_id.assert_called_once_with(order.id)
        order_service.repository.update_order.assert_called_once_with(order)

        assert order_service.product_service.release_stock.call_count == 2
        order_service.product_service.release_stock.assert_has_calls(
            [
                call(mock_order_item1.product_id, mock_order_item1.quantity),
                call(mock_order_item2.product_id, mock_order_item2.quantity),
            ],
            any_order=False
        )


        assert len(result_dto.items) == 2
        assert result_dto.items[0].id == mock_order_item1.id
        assert result_dto.items[0].product.id == mock_product1.id
        assert result_dto.items[1].id == mock_order_item2.id
        assert result_dto.items[1].product.id == mock_product2.id
        assert result_dto.status == OrderStatus.CANCELED
        


    