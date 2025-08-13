from uuid import uuid4
from apps.carts.service import CartService
from apps.carts.entity import Cart, CartItem
from unittest.mock import MagicMock
from apps.shared.exceptions import ConflictError, NotFoundError
import pytest


mock_repository = MagicMock()
mock_product_service = MagicMock()
mock_user_service = MagicMock()
mock_logger = MagicMock()
mock_user = MagicMock()
mock_product = MagicMock()
service = CartService(mock_repository, mock_product_service, mock_user_service, mock_logger)

def reset_mocks():
        mock_product_service.reset_mock()
        mock_user_service.reset_mock()
        mock_repository.reset_mock()
        mock_logger.reset_mock()


@pytest.fixture
def test_cart():
    return Cart(mock_user.id)


class TestCartCreation:
    def test_should_create_new_cart_successfully(self, test_cart):
        mock_repository.save.return_value = test_cart
        cart = service.create_cart(mock_user.id)
        mock_repository.save.assert_called_once()
        assert isinstance(cart.items, list)
        assert len(cart.items) == 0
        assert cart.user_id == mock_user.id
        mock_logger.info.assert_called_once()
        assert "Cart successfully created" in mock_logger.info.call_args[0][0]


class TestCartAddProduct:
    def test_should_add_product_to_existing_user_cart_successfully(self, test_cart):
        mock_product = MagicMock()
        quantity = 1

        mock_user_service.get_user_by_id.return_value = mock_user
        mock_repository.get_cart_by_user.return_value = test_cart
        mock_product_service.get_product_by_id.return_value = mock_product

        updated_cart = service.add_to_cart(mock_user.id, mock_product.id, quantity)

        mock_product_service.get_product_by_id.assert_called_once_with(mock_product.id)
        mock_user_service.get_user_by_id.assert_called_once_with(mock_user.id)
        mock_repository.get_cart_by_user.assert_called_once_with(mock_user.id)
        mock_repository.update.assert_called_once_with(test_cart)

        assert len(updated_cart.items) == 1
        assert isinstance(updated_cart.items[0], CartItem)
        assert updated_cart.items[0].product.id == mock_product.id
        assert updated_cart.items[0].quantity == quantity
        reset_mocks()


    def test_should_add_product_to_new_user_cart_successfully(self, test_cart):
        quantity = 1

        mock_user_service.get_user_by_id.return_value = mock_user
        mock_repository.get_cart_by_user.return_value = None
        mock_repository.save.return_value = test_cart
        mock_product_service.get_product_by_id.return_value = mock_product

        updated_cart = service.add_to_cart(mock_user.id, mock_product.id, quantity)

        mock_product_service.get_product_by_id.assert_called_once_with(mock_product.id)
        mock_user_service.get_user_by_id.assert_called_once_with(mock_user.id)
        mock_repository.get_cart_by_user.assert_called_once_with(mock_user.id)
        mock_repository.update.assert_called_once_with(test_cart)

        assert len(updated_cart.items) == 1
        assert isinstance(updated_cart.items[0], CartItem)
        assert updated_cart.items[0].product.id == mock_product.id
        assert updated_cart.items[0].quantity == quantity
        reset_mocks()


class TestCartSubtractItemQuantity:
     def test_should_subtract_cart_item_quantity_successfully(self):
        quantity_to_subtract = 1
        cart_item = CartItem(mock_product, 3)
        cart_with_item = Cart(mock_user.id, [cart_item])
        mock_repository.get_cart_by_user.return_value = cart_with_item

        cart = service.subtract_quantity_from_cart_item(mock_user.id, mock_product.id, quantity_to_subtract)

        mock_repository.get_cart_by_user.assert_called_once_with(mock_user.id)
        mock_repository.update.assert_called_once_with(cart_with_item)
        assert cart.items[0].quantity == 2

     def test_should_raise_conflict_error_for_quantity_greater_than_cart_item_quantity(self):
        quantity_to_subtract = 4
        cart_item = CartItem(mock_product, 3)
        cart_with_item = Cart(mock_user.id, [cart_item])
        mock_repository.get_cart_by_user.return_value = cart_with_item

        with pytest.raises(ConflictError) as exc:
            service.subtract_quantity_from_cart_item(mock_user.id, mock_product.id, quantity_to_subtract)
        assert "Quantity cannot be negative" in str(exc)

     def test_should_raise_not_found_error_for_non_existent_product(self):
        quantity_to_subtract = 1
        cart_item = CartItem(mock_product, 3)
        cart_with_item = Cart(mock_user.id, [cart_item])
        mock_repository.get_cart_by_user.return_value = cart_with_item

        with pytest.raises(NotFoundError) as exc:
            service.subtract_quantity_from_cart_item(mock_user.id, uuid4(), quantity_to_subtract)
        assert "not found in cart" in str(exc)