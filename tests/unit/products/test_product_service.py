from datetime import datetime
from apps.products.service import ProductService
from apps.products.product_entity import Product
from uuid import UUID, uuid4
from apps.shared.value_objects import Price, Stock, Title, Description
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

        return title, description, price, stock, owner_id

@pytest.fixture
def mock_product(product_args):
        title, description, price, stock, owner_id = product_args
        mock_product = Product(title, description, price, stock, owner_id, uuid4(), True, datetime.now(), datetime.now())
        return mock_product


class TestProductService:
    def test_should_create_product_with_valid_data(self, product_args, mock_product):
        title, description, price, stock, owner_id = product_args

        mock_repository = MagicMock()

        mock_repository.save.return_value = mock_product

        service = ProductService(mock_repository)


        product = service.create_product(
            title=title,
            description=description,
            price=price,
            stock=stock,
            owner_id=owner_id
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
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
        mock_repository.save.assert_called_once

    def test_should_get_product_by_id_successfully(self, product_args, mock_product):
        title, description, price, stock, owner_id = product_args

        mock_repository = MagicMock()

        service = ProductService(mock_repository)

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
        assert retrieved_product.is_active is True
        assert retrieved_product.created_at is not None
        assert retrieved_product.updated_at is not None
        mock_repository.get_product_by_id.assert_called_once_with(mock_product.id)