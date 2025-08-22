from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from apps.products.product_entity import Product
from apps.products.schema import ProductActivationSchema, ProductUpdateSchema
from apps.products.service import ProductService
from apps.shared.exceptions import NotFoundError
from apps.shared.value_objects import Description, Price, Stock, Title
from apps.categories.entity import Category


mock_category_service = MagicMock()
mock_user_service = MagicMock()
mock_user = MagicMock()
mock_logger = MagicMock()

cat_name = "Category"
cat_desc = "Cat desc"
test_category = Category(name=cat_name, description=cat_desc)
categories = [ test_category ]

def assert_list_has_valid_categories(test_categories: list[Category]):
    assert isinstance(test_categories, list)
    assert isinstance(test_categories[0], Category)
    assert test_categories[0].name == cat_name
    assert test_categories[0].description == cat_desc

@pytest.fixture
def product_args():
    title = "title"
    description = "description"
    price = "1.99"
    stock = 5
    owner_id = mock_user.id

    return title, description, price, stock, owner_id


@pytest.fixture
def test_product(product_args):
    title, description, price, stock, owner_id = product_args
    test_product = Product(
        Title(title),
        Description(description),
        Price(price),
        Stock(stock),
        owner_id,
        categories,
        uuid4(),
        True,
        datetime.now(),
        datetime.now(),
    )
    return test_product

@pytest.fixture
def mock_repository_and_service():
    mock_repository = MagicMock()
    service = ProductService(mock_repository, mock_logger, mock_category_service, mock_user_service)
    return mock_repository, service


@pytest.fixture
def update_product():
    def _update_product(service, product_id, payload):
        payload_schema = ProductUpdateSchema(**payload)
        service.update_product(product_id, payload_schema)

    return _update_product


class TestProductCreation:
    def test_should_create_product_with_valid_data(
        self, product_args, test_product, mock_repository_and_service
    ):
        title, description, price, stock, owner_id = product_args
        mock_repository, service = mock_repository_and_service

        mock_user_service.get_user_by_id.return_value = mock_user
        mock_category_service.get_category_by_id.return_value = test_category
        mock_repository.save.return_value = test_product

        product = service.create_product(
            title=title,
            description=description,
            price=price,
            stock=stock,
            owner_id=owner_id,
            categories_ids=[ test_category.id ],
        )

        assert isinstance(product, Product)
        assert isinstance(product.id, UUID)
        assert product.title == Title(title)
        assert product.description == Description(description)
        assert product.price == Price(price)
        assert product.stock == Stock(stock)
        assert product.owner_id == owner_id
        assert_list_has_valid_categories(product.categories)
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
        mock_repository.save.assert_called_once()
        mock_logger.info.assert_called_once()
        assert "Product successfully created" in mock_logger.info.call_args[0][0]

class TestGetProductById:
    def test_should_get_product_by_id_successfully(
        self, product_args, test_product, mock_repository_and_service
    ):
        mock_logger.reset_mock()
        title, description, price, stock, owner_id = product_args

        mock_repository, service = mock_repository_and_service

        mock_repository.get_product_by_id.return_value = test_product

        retrieved_product = service.get_product_by_id(test_product.id)

        assert isinstance(retrieved_product, Product)
        assert isinstance(retrieved_product.id, UUID)
        assert isinstance(retrieved_product.title, Title)
        assert retrieved_product.title.value == title
        assert retrieved_product.description == Description(description)
        assert retrieved_product.price == Price(price)
        assert retrieved_product.stock == Stock(stock)
        assert retrieved_product.owner_id == owner_id
        assert_list_has_valid_categories(retrieved_product.categories)
        assert retrieved_product.is_active is True
        assert retrieved_product.created_at is not None
        assert retrieved_product.updated_at is not None
        mock_repository.get_product_by_id.assert_called_once_with(test_product.id)

    def test_should_raise_not_found_error_for_invalid_id(
        self, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_repository.get_product_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc:
            service.get_product_by_id(uuid4())

        assert "not found" in str(exc)
        mock_logger.warning.assert_called_once()
        assert "not found" in mock_logger.warning.call_args[0][0]


class TestListProductsByCategory:
    def test_should_list_products_by_category_successfully(
        self, product_args, test_product, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_repository.list_products_by_category.return_value = [test_product]

        products = service.list_products_by_category(category_id=test_product.id)

        assert mock_repository.list_products_by_category.assert_called_once
        assert test_product in products

class TestProductUpdate:
    def test_should_update_product(self, mock_repository_and_service, update_product):
        mock_repository, service = mock_repository_and_service

        mock_product = MagicMock()

        mock_repository.get_product_by_id.return_value = mock_product

        title_payload = {"title": "Changed title"}
        update_product(service, mock_product.id, title_payload)

        mock_repository.get_product_by_id.assert_called_once_with(mock_product.id)
        mock_product.change_title.assert_called_once_with(title_payload["title"])
        mock_repository.update_product.assert_called_once_with(mock_product)
        mock_logger.info.assert_called_once()
        assert "Product successfully updated" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()

        description_payload = {"description": "new description"}
        update_product(service, mock_product.id, description_payload)
        mock_product.change_description.assert_called_once_with(
            description_payload["description"]
        )
        mock_logger.info.assert_called_once()
        assert "Product successfully updated" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()

        price_payload = {"price": "2.99"}
        update_product(service, mock_product.id, price_payload)
        mock_product.change_price.assert_called_once_with(price_payload["price"])
        mock_logger.info.assert_called_once()
        assert "Product successfully updated" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()

        stock_payload = {"stock": 3}
        update_product(service, mock_product.id, stock_payload)
        mock_product.change_stock.assert_called_once_with(stock_payload["stock"])
        mock_logger.info.assert_called_once()
        assert "Product successfully updated" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()

        category_payload = {"categories": [uuid4()]}
        update_product(service, mock_product.id, category_payload)
        mock_product.change_categories.assert_called_once()
        mock_logger.info.assert_called_once()
        assert "Product successfully updated" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()


    def test_should_raise_not_found_error_on_update_product_with_invalid_id(
        self, mock_repository_and_service, update_product
    ):
        mock_repository, service = mock_repository_and_service
        mock_repository.get_product_by_id.return_value = None

        title_payload = {"title": "Changed title"}
        with pytest.raises(NotFoundError) as exc:
            update_product(service, uuid4(), title_payload)

        assert "Product not found" in str(exc)
        mock_logger.warning.assert_called_once()
        assert "Product not found" in mock_logger.warning.call_args[0][0]

class TestProductActivation:
    def test_should_activate_and_deactivate_product_successfully(
        self, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_product = MagicMock()

        mock_repository.get_product_by_id.return_value = mock_product

        activate_payload = ProductActivationSchema(status=True)
        service.product_activation(mock_product.id, activate_payload)
        mock_product.activate.assert_called_once()
        
        mock_logger.info.assert_called_once()
        assert "activated successfully" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()

        deactivate_payload = ProductActivationSchema(status=False)
        service.product_activation(mock_product.id, deactivate_payload)
        mock_product.deactivate.assert_called_once()

        mock_repository.get_product_by_id.assert_called_with(mock_product.id)
        mock_repository.update_product.assert_called_with(mock_product)
        assert mock_repository.get_product_by_id.call_count == 2
        assert mock_repository.update_product.call_count == 2
        mock_logger.info.assert_called_once()
        assert "deactivated successfully" in mock_logger.info.call_args[0][0]
        mock_logger.reset_mock()


    def test_should_raise_not_found_error_on_deactivate_invalid_product_id(
        self, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_repository.get_product_by_id.return_value = None

        activate_payload = ProductActivationSchema(status=True)

        with pytest.raises(NotFoundError) as exc:
            service.product_activation(uuid4(), activate_payload)
        assert "not found" in str(exc)
        mock_logger.warning.assert_called_once()
        assert "Product not found" in mock_logger.warning.call_args[0][0]

class TestProductDeletion:
    def test_should_delete_product_successfully(self, mock_repository_and_service):
        mock_repository, service = mock_repository_and_service
        mock_product = MagicMock()
        mock_repository.get_product_by_id.return_value = mock_product

        service.delete_product(mock_product.id)

        mock_repository.get_product_by_id.assert_called_once_with(mock_product.id)
        mock_repository.delete_product.assert_called_once_with(mock_product)
        mock_logger.info.assert_called_once()
        assert "Product successfully deleted" in mock_logger.info.call_args[0][0]

    def test_should_raise_not_found_error_to_delete_invalid_product_id(self, mock_repository_and_service):
        mock_logger.reset_mock()
        mock_repository, service = mock_repository_and_service
        mock_repository.get_product_by_id.return_value = None

        with pytest.raises(NotFoundError) as exc:
            service.delete_product(uuid4())

        mock_logger.warning.assert_called_once()
        assert "Not found Product" in mock_logger.warning.call_args[0][0]
        assert "not found" in str(exc)

class TestProductStockReservation:
    def test_should_update_stock_with_remaining_quantity(self, test_product, mock_repository_and_service):
        mock_repository, service = mock_repository_and_service
        reserved_quantity = 3
        mock_product = MagicMock()
        mock_product.stock.value = 5
        mock_repository.get_product_for_update.return_value = mock_product

        service.reserve_stock(test_product.id, reserved_quantity)

        mock_repository.get_product_for_update.assert_called_once_with(test_product.id)
        mock_product.change_stock.assert_called_once()
        mock_repository.update_product.assert_called_once_with(mock_product)
    
    def test_should_raise_not_found_error_for_invalid_product_id(self, mock_repository_and_service):
        mock_repository, service = mock_repository_and_service
        reserved_quantity = 3
        mock_repository.get_product_for_update.return_value = None
        
        with pytest.raises(NotFoundError) as exc:
            service.reserve_stock(uuid4(), reserved_quantity)

        assert "Product not found" in str(exc)
        assert "Product not found" in mock_logger.warning.call_args[0][0]
        