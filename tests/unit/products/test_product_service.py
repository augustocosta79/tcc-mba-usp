from datetime import datetime
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from apps.products.product_entity import Product
from apps.products.schema import ProductActivationSchema, ProductUpdateSchema
from apps.products.service import ProductService
from apps.shared.exceptions import NotFoundError
from apps.shared.value_objects import Description, Price, Stock, Title


@pytest.fixture
def product_args():
    title = "title"
    description = "description"
    price = "1.99"
    stock = 5
    owner_id = uuid4()
    category = "test"

    return title, description, price, stock, owner_id, category


@pytest.fixture
def test_product(product_args):
    title, description, price, stock, owner_id, category = product_args
    test_product = Product(
        Title(title),
        Description(description),
        Price(price),
        Stock(stock),
        owner_id,
        category,
        uuid4(),
        True,
        datetime.now(),
        datetime.now(),
    )
    return test_product


@pytest.fixture
def mock_repository_and_service():
    mock_repository = MagicMock()
    service = ProductService(mock_repository)
    return mock_repository, service


@pytest.fixture
def update_product():
    def _update_product(service, product_id, payload):
        payload_schema = ProductUpdateSchema(**payload)
        service.update_product(product_id, payload_schema)

    return _update_product


class TestProductService:
    def test_should_create_product_with_valid_data(
        self, product_args, test_product, mock_repository_and_service
    ):
        title, description, price, stock, owner_id, category = product_args

        mock_repository, service = mock_repository_and_service

        mock_repository.save.return_value = test_product

        product = service.create_product(
            title=title,
            description=description,
            price=price,
            stock=stock,
            owner_id=owner_id,
            category=category,
        )

        assert isinstance(product, Product)
        assert isinstance(product.id, UUID)
        assert product.title == Title(title)
        assert product.description == Description(description)
        assert product.price == Price(price)
        assert product.stock == Stock(stock)
        assert product.owner_id == owner_id
        assert product.category == category
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
        mock_repository.save.assert_called_once

    def test_should_get_product_by_id_successfully(
        self, product_args, test_product, mock_repository_and_service
    ):
        title, description, price, stock, owner_id, category = product_args

        mock_repository, service = mock_repository_and_service

        mock_repository.get_product_by_id.return_value = test_product

        retrieved_product = service.get_product_by_id(test_product.id)

        assert isinstance(retrieved_product, Product)
        assert isinstance(retrieved_product.id, UUID)
        assert isinstance(retrieved_product.title, Title)
        assert retrieved_product.title.text == title
        assert retrieved_product.description == Description(description)
        assert retrieved_product.price == Price(price)
        assert retrieved_product.stock == Stock(stock)
        assert retrieved_product.owner_id == owner_id
        assert retrieved_product.category == category
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

    def test_should_list_products_by_category_successfully(
        self, product_args, test_product, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_repository.list_products_by_category.return_value = [test_product]

        products = service.list_products_by_category(category="test")

        assert mock_repository.list_products_by_category.assert_called_once
        assert test_product in products

    def test_should_update_product(self, mock_repository_and_service, update_product):
        mock_repository, service = mock_repository_and_service

        mock_product = MagicMock()

        mock_repository.get_product_by_id.return_value = mock_product

        title_payload = {"title": "Changed title"}
        update_product(service, mock_product.id, title_payload)

        mock_repository.get_product_by_id.assert_called_once_with(mock_product.id)
        mock_product.change_title.assert_called_once_with(title_payload["title"])
        mock_repository.update_product.assert_called_once_with(mock_product)

        description_payload = {"description": "new description"}
        update_product(service, mock_product.id, description_payload)
        mock_product.change_description.assert_called_once_with(
            description_payload["description"]
        )

        price_payload = {"price": "2.99"}
        update_product(service, mock_product.id, price_payload)
        mock_product.change_price.assert_called_once_with(price_payload["price"])

        stock_payload = {"stock": 3}
        update_product(service, mock_product.id, stock_payload)
        mock_product.change_stock.assert_called_once_with(stock_payload["stock"])

        category_payload = {"category": str(uuid4())}
        update_product(service, mock_product.id, category_payload)
        mock_product.change_category.assert_called_once_with(
            category_payload["category"]
        )

    def test_should_raise_not_found_error_on_update_product_with_invalid_id(
        self, mock_repository_and_service, update_product
    ):
        mock_repository, service = mock_repository_and_service
        mock_repository.get_product_by_id.return_value = None

        title_payload = {"title": "Changed title"}
        with pytest.raises(NotFoundError) as exc:
            update_product(service, uuid4(), title_payload)

        assert "not found" in str(exc)

    def test_should_activate_and_deactivate_product_successfully(
        self, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_product = MagicMock()

        mock_repository.get_product_by_id.return_value = mock_product

        activate_payload = ProductActivationSchema(status=True)
        service.product_activation(mock_product.id, activate_payload)
        mock_product.activate.assert_called_once

        deactivate_payload = ProductActivationSchema(status=False)
        service.product_activation(mock_product.id, deactivate_payload)
        mock_product.deactivate.assert_called_once

        mock_repository.get_product_by_id.assert_called_with(mock_product.id)
        mock_repository.update_product.assert_called_with(mock_product)
        assert mock_repository.get_product_by_id.call_count == 2
        assert mock_repository.update_product.call_count == 2

    def test_should_raise_not_found_error_on_deactivate_invalid_product_id(
        self, mock_repository_and_service
    ):
        mock_repository, service = mock_repository_and_service

        mock_repository.get_product_by_id.return_value = None

        activate_payload = ProductActivationSchema(status=True)

        with pytest.raises(NotFoundError) as exc:
            service.product_activation(uuid4(), activate_payload)
        assert "not found" in str(exc)
