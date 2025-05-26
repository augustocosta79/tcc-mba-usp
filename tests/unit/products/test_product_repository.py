from datetime import datetime
from uuid import UUID, uuid4
from apps.shared.value_objects import Title, Description, Price, Stock
from apps.products.product_entity import Product
from apps.products.repository import ProductRepository
import pytest


@pytest.fixture
def create_product_and_repository():
    title_string = "Title test"
    title = Title(title_string)

    description_string = "some description"
    description = Description(description_string)

    price_value = "1.99"
    price = Price(price_value)

    stock_value = 5
    stock = Stock(stock_value)

    owner_id = uuid4()

    product = Product(
        title,
        description,
        price,
        stock,
        owner_id
    )

    repository = ProductRepository()

    return product, repository


@pytest.mark.django_db
class TestProductRepository:
    def test_should_save_product_successfully(self, create_product_and_repository):
        product, repository = create_product_and_repository

        saved_product = repository.save(product)

        assert isinstance(saved_product, Product)
        assert saved_product.id == product.id
        assert isinstance(saved_product.title, Title)
        assert saved_product.title == product.title
        assert saved_product.description == product.description
        assert saved_product.price == product.price
        assert saved_product.stock == product.stock
        assert isinstance(saved_product.owner_id, UUID)
        assert saved_product.owner_id == product.owner_id

    def test_should_get_product_by_id(self, create_product_and_repository):
        product, repository = create_product_and_repository
        repository.save(product)

        retrieved_product = repository.get_product_by_id(product.id)

        assert retrieved_product is not None
        assert retrieved_product.id == product.id
        assert retrieved_product.title == product.title
        assert retrieved_product.description == product.description
        assert retrieved_product.price == product.price
        assert retrieved_product.stock == product.stock
        assert retrieved_product.is_active is product.is_active
        assert retrieved_product.created_at is not None
        assert retrieved_product.updated_at is not None
        assert isinstance(retrieved_product.created_at, datetime)
        assert isinstance(retrieved_product.updated_at, datetime)




