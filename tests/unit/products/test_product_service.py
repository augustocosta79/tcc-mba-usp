from datetime import datetime
from apps.products.service import ProductService
from apps.products.product_entity import Product
from uuid import UUID, uuid4
from apps.shared.value_objects import Price, Stock, Title, Description
from apps.products.schema import ProductUpdateSchema
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def product_args():
        title_string = "title"
        title = Title(title_string)
        description_string = "description"
        description = Description(description_string)
        price = Price("1.99")
        stock_value = 5
        stock = Stock(stock_value)
        owner_id = uuid4()
        category = "test"

        return title, description, price, stock, owner_id, category

@pytest.fixture
def mock_product(product_args):
        title, description, price, stock, owner_id, category = product_args
        mock_product = Product(title, description, price, stock, owner_id, category, uuid4(), True, datetime.now(), datetime.now())
        return mock_product

@pytest.fixture
def mock_repository_and_service():
    mock_repository = MagicMock()
    service = ProductService(mock_repository)
    return mock_repository, service


class TestProductService:
    def test_should_create_product_with_valid_data(self, product_args, mock_product, mock_repository_and_service):
        title, description, price, stock, owner_id, category = product_args

        mock_repository, service = mock_repository_and_service

        mock_repository.save.return_value = mock_product



        product = service.create_product(
            title=title,
            description=description,
            price=price,
            stock=stock,
            owner_id=owner_id,
            category=category
        )
        print(product)

        assert isinstance(product, Product)
        assert isinstance(product.id, UUID)
        assert product.title.text == title.text
        assert product.description == description
        assert product.description.text == description.text
        assert product.price == price
        assert product.stock == stock
        assert product.stock.value == stock.value
        assert product.owner_id == owner_id
        assert product.category == category
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
        mock_repository.save.assert_called_once

    def test_should_get_product_by_id_successfully(self, product_args, mock_product, mock_repository_and_service):
        title, description, price, stock, owner_id, category = product_args

        mock_repository, service = mock_repository_and_service

        mock_repository.get_product_by_id.return_value = mock_product

        retrieved_product = service.get_product_by_id(mock_product.id)

        assert isinstance(retrieved_product, Product)
        assert isinstance(retrieved_product.id, UUID)
        assert retrieved_product.title.text == title.text
        assert retrieved_product.description == description
        assert retrieved_product.description.text == description.text
        assert retrieved_product.price == price
        assert retrieved_product.stock == stock
        assert retrieved_product.stock.value == stock.value
        assert retrieved_product.owner_id == owner_id
        assert retrieved_product.category == category
        assert retrieved_product.is_active is True
        assert retrieved_product.created_at is not None
        assert retrieved_product.updated_at is not None
        mock_repository.get_product_by_id.assert_called_once_with(mock_product.id)

    def test_should_list_products_by_category_successfully(self, product_args, mock_product, mock_repository_and_service):
          mock_repository, service  = mock_repository_and_service

          mock_repository.list_products_by_category.return_value = [mock_product]

          products = service.list_products_by_category(category="test")

          assert mock_repository.list_products_by_category.assert_called_once
          assert mock_product in products


    def test_should_update_product(self, mock_repository_and_service):
            mock_repository, service = mock_repository_and_service

            mock_product = MagicMock()

            mock_repository.get_product_by_id.return_value = mock_product

            title_payload = {"title": "Changed title"}
            payload_schema = ProductUpdateSchema(**title_payload)

            service.update_product(mock_product.id, payload_schema)

            mock_repository.get_product_by_id.assert_called_once()
            mock_product.change_title.assert_called_once_with(title_payload["title"])
            mock_repository.update_product.assert_called_once_with(mock_product)

