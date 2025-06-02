from datetime import datetime
from decimal import Decimal
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

    category = "test"

    product = Product(
        title,
        description,
        price,
        stock,
        owner_id,
        category
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

    def test_should_list_products_by_category(self, create_product_and_repository):
        product, repository = create_product_and_repository
        saved_product = repository.save(product)

        products = repository.list_products_by_category(category=product.category)

        assert isinstance(products, list)
        assert len(products) == 1
        assert products[0].id == saved_product.id

    def test_should_update_persisted_product_data_successfully(self, create_product_and_repository):
        product, repository = create_product_and_repository
        repository.save(product)

        new_title = "changed title"
        product.change_title(new_title)
        updated_product = repository.update_product(product)
        
        assert isinstance(updated_product, Product)
        assert updated_product.title == Title(new_title)
        assert updated_product.title.text == new_title
        assert updated_product.id == product.id

        new_description = "changed description"
        product.change_description(new_description)
        updated_product = repository.update_product(product)
        assert updated_product.description == Description(new_description)
        assert updated_product.description.text == new_description

        new_price = "2.99"
        product.change_price(new_price)
        updated_product = repository.update_product(product)
        assert updated_product.price == Price(new_price)
        assert updated_product.price.value == Decimal(new_price)

        new_stock = 1
        product.change_stock(new_stock)
        updated_product = repository.update_product(product)
        assert updated_product.stock == Stock(new_stock)
        assert updated_product.stock.value == new_stock






