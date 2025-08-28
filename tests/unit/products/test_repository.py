from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from apps.users.repository import UserRepository
from apps.users.service import UserService
import pytest
from apps.products.product_entity import Product
from apps.products.repository import ProductRepository
from apps.shared.value_objects import Description, Price, Stock, Title
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from utils.logger import configure_logger
from apps.categories.entity import Category
from django.db import connection, transaction

import threading
from time import sleep

from django.test import TransactionTestCase
from apps.products.models import ProductModel
from apps.shared.exceptions import OutOfStockError
from apps.products.product_entity import Product

logger = configure_logger(__name__)
repository = CategoryRepository()
category_service = CategoryService(repository, logger)
cat_name = "category"
cat_desc = "description"

@pytest.mark.django_db
@pytest.fixture
def categories():
    category = category_service.create_category(cat_name, cat_desc)
    categories = [ category ]
    return categories

@pytest.fixture
def test_user():
    repository = UserRepository()
    service = UserService(repository, logger)
    user = service.create_user("test user", "email@test.com", "Abc@1234", "usernameTest")
    return user

@pytest.fixture
def create_product_and_repository(categories, test_user):
    title_string = "Title test"
    title = Title(title_string)

    description_string = "some description"
    description = Description(description_string)

    price_value = "1.99"
    price = Price(price_value)

    stock_value = 5
    stock = Stock(stock_value)

    owner_id = test_user.id

    product = Product(title, description, price, stock, owner_id, categories)

    repository = ProductRepository()

    return product, repository


@pytest.mark.django_db
class TestProductRepository:
    def test_should_save_product_successfully(self, create_product_and_repository, categories):
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
        assert isinstance(saved_product.categories, list)
        assert isinstance(saved_product.categories[0], Category)
        assert saved_product.categories[0].id == categories[0].id
        assert saved_product.categories[0].name.value == categories[0].name.value
        assert saved_product.categories[0].description.value == categories[0].description.value
        

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

        products = repository.list_products_by_category(category_id=saved_product.categories[0].id)

        assert isinstance(products, list)
        assert len(products) == 1
        assert products[0].id == saved_product.id

    def test_should_update_persisted_product_data_successfully(
        self, create_product_and_repository
    ):
        test_product, repository = create_product_and_repository
        product = repository.save(test_product)

        new_title = "changed title"
        product.change_title(new_title)
        updated_product = repository.update_product(product)
        assert isinstance(updated_product, Product)
        assert updated_product.title == Title(new_title)
        assert updated_product.title.value == new_title
        assert updated_product.id == product.id
        assert updated_product.updated_at > product.updated_at

        new_description = "changed description"
        product.change_description(new_description)
        updated_product = repository.update_product(product)
        assert updated_product.description == Description(new_description)
        assert updated_product.description.value == new_description
        assert updated_product.updated_at > product.updated_at

        new_price = "2.99"
        product.change_price(new_price)
        updated_product = repository.update_product(product)
        assert updated_product.price == Price(new_price)
        assert updated_product.price.value == Decimal(new_price)
        assert updated_product.updated_at > product.updated_at

        new_category = category_service.create_category("new cat", "new desc")
        product.change_categories([new_category])
        updated_product = repository.update_product(product)
        assert updated_product.categories[0].id == new_category.id
        assert updated_product.categories[0].name.value == new_category.name.value
        assert updated_product.categories[0].description.value == new_category.description.value
        assert updated_product.updated_at > product.updated_at

        product.deactivate()
        updated_product = repository.update_product(product)
        assert updated_product.is_active is False
        assert updated_product.updated_at > product.updated_at

        product.activate()
        updated_product = repository.update_product(product)
        assert updated_product.is_active is True
        assert updated_product.updated_at > product.updated_at

    def test_should_delete_product_successfully(self, create_product_and_repository):
        product, repository = create_product_and_repository
        repository.delete_product(product)

        assert repository.get_product_by_id(product.id) is None



    @pytest.mark.django_db(transaction=True)
    def test_debit_stock_concurrently_should_lock_and_preserve_consistency(self, create_product_and_repository):
        product, repository = create_product_and_repository
        saved_product = repository.save(product)

        result = {}

        def debit_stock(quantity, transaction_id, sleep_time):
            try:
                sleep(sleep_time)
                with transaction.atomic():
                    reserved_product = repository.get_product_for_update(saved_product.id)
                    result[f"{transaction_id}_before"] = reserved_product.stock.value
                    reserved_product.reserve_stock(quantity)
                    repository.update_product(reserved_product)
                    result[f"{transaction_id}_after"] = reserved_product.stock.value
            finally:
                    connection.close()


        t1 = threading.Thread(target=debit_stock, args=(2, "t1", 0))
        t2 = threading.Thread(target=debit_stock, args=(1, "t2", 0.5))

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert result["t1_before"] == 5
        assert result["t1_after"] == 3
        assert result["t2_before"] == 3
        assert result["t2_after"] == 2

        
