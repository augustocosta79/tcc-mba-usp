from datetime import datetime
from uuid import UUID, uuid4

from apps.categories.repository import CategoryRepository
from apps.categories.service import CategoryService
from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.products.repository import ProductRepository
import pytest
from apps.products.service import ProductService
from tests.utils.timed_client import TimedClient

from tests.utils.assertions import assert_has_valid_id, assert_has_valid_timestamps

from utils.logger import configure_logger
logger = configure_logger(__name__)


@pytest.fixture
def timed_client(client):
    return TimedClient(client)


@pytest.fixture
def test_user():
    repository = UserRepository()
    service = UserService(repository, logger)
    user = service.create_user("test user", "email@test.com", "Abc@1234", "usernameTest")
    return user


@pytest.fixture
def create_product_parameters(test_user):
    title = "valid Title"
    description = "valid desctiprion"
    price = "1.99"
    stock = 5
    owner_id = test_user.id

    return title, description, price, stock, owner_id


@pytest.mark.django_db
@pytest.fixture
def create_test_category():
    def _create(name="category", description="description"):
        repository = CategoryRepository()
        service = CategoryService(repository, logger)
        return service.create_category(name, description)
    return _create



@pytest.fixture
def create_test_product(create_product_parameters, create_test_category):
    repository = ProductRepository()
    service = ProductService(repository, logger)

    test_category = create_test_category()

    title, description, price, stock, owner_id = create_product_parameters

    product = service.create_product(
        title, description, price, stock, owner_id, [test_category.id]
    )

    return product


@pytest.mark.django_db
class TestCreateProduct:
    def test_should_return_status_201_created_and_product_data(self, timed_client, create_test_category, test_user):
        test_category = create_test_category()
        valid_payload = {
            "title": "valid Title",
            "description": "valid description",
            "price": "1.99",
            "stock": 3,
            "owner_id": str(test_user.id),
            "categories": [str(test_category.id)],
        }

        response = timed_client.post(
            "/api/products", valid_payload, content_type="application/json"
        )
        assert response.status_code == 201

        body = response.json()

        assert_has_valid_id(body)
        assert body["title"] == valid_payload["title"]
        assert body["description"] == valid_payload["description"]
        assert body["price"] == valid_payload["price"]
        assert body["stock"] == valid_payload["stock"]
        assert body["owner_id"] == valid_payload["owner_id"]
        assert body["categories"][0]["id"] == str(test_category.id)
        assert body["categories"][0]["name"] == test_category.name.value
        assert body["categories"][0]["description"] == test_category.description.value
        assert "created_at" in body
        assert "updated_at" in body
        assert_has_valid_timestamps(body)


@pytest.mark.django_db
class TestGetProductbyId:
    def test_should_return_status_200_ok_and_product_data(
        self, timed_client, create_test_product, test_user
    ):
        existing_product = create_test_product

        response = timed_client.get(f"/api/products/{existing_product.id}")

        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(existing_product.id)
        assert body["title"] == existing_product.title.value
        assert body["description"] == existing_product.description.value
        assert body["price"] == str(existing_product.price.value)
        assert body["stock"] == existing_product.stock.value
        assert body["owner_id"] == str(test_user.id)
        assert body["categories"][0]["id"] == str(existing_product.categories[0].id)
        assert body["categories"][0]["name"] == str(existing_product.categories[0].name)
        assert body["categories"][0]["description"] == str(existing_product.categories[0].description)
        assert body["is_active"] is existing_product.is_active
        assert_has_valid_timestamps(body)


    def test_should_return_404_not_found_for_invalid_product_id(
        self, timed_client, create_test_product, test_user
    ):
        response = timed_client.get(f"/api/products/{uuid4()}")
        assert response.status_code == 404
        assert "not found" in response.json()["message"]


@pytest.mark.django_db
class TestGetProductByCategory:
    def test_should_return_status_200_ok_and_list_products_data_by_category(
        self, timed_client, create_test_product
    ):
        product = create_test_product

        response = timed_client.get("/api/products", {"category_id": product.categories[0].id})
        assert response.status_code == 200

        body = response.json()

        assert isinstance(body, list)
        assert len(body) == 1
        assert body[0]["id"] == str(product.id)
        assert body[0]["categories"][0]["id"] == str(product.categories[0].id)
        assert_has_valid_timestamps(body[0])


@pytest.fixture
def send_update_request():
    def _send_update_request(timed_client, product_id, payload):
        response = timed_client.patch(
            f"/api/products/{product_id}", payload, content_type="application/json"
        )
        assert response.status_code == 200
        body = response.json()

        return body

    return _send_update_request


@pytest.mark.django_db
class TestUpdateProduct:
    def test_should_return_status_200_ok_and_updated_product_data(
        self, timed_client, create_test_product, send_update_request, create_test_category
    ):
        product = create_test_product
        create_test_category()

        title_payload = {"title": "changed title"}
        body = send_update_request(timed_client, product.id, title_payload)

        assert body["id"] == str(product.id)
        assert body["title"] == title_payload["title"]
        assert body["description"] == product.description.value
        assert body["price"] == str(product.price.value)
        assert body["stock"] == product.stock.value
        assert body["owner_id"] == str(product.owner_id)
        assert body["categories"][0]["id"] == str(product.categories[0].id)
        assert body["is_active"] is product.is_active
        assert_has_valid_timestamps(body)

        description_payload = {"description": "changed description"}
        body = send_update_request(timed_client, product.id, description_payload)
        assert body["description"] == description_payload["description"]

        price_payload = {"price": "1.99"}
        body = send_update_request(timed_client, product.id, price_payload)
        assert body["price"] == price_payload["price"]

        stock_payload = {"stock": 3}
        body = send_update_request(timed_client, product.id, stock_payload)
        assert body["stock"] == stock_payload["stock"]

        new_cat_name = "new category"
        new_cat_desc = "new description"
        new_category = create_test_category(new_cat_name, new_cat_desc)
        category_payload = {"categories": [str(new_category.id)]}
        body = send_update_request(timed_client, product.id, category_payload)
        assert body["categories"][0]["name"] == new_cat_name
        assert body["categories"][0]["id"] == category_payload["categories"][0]

    def test_should_return_status_404_invalid_product_id(self, timed_client):
        response = timed_client.patch(
            f"/api/products/{uuid4()}", {'title': 'testing'}, content_type="application/json"
        )
        assert response.status_code == 404
        assert "not found" in response.json()["message"]


@pytest.mark.django_db
class TestProductActivation:
    def test_should_return_status_200_ok_and_activate_product_successfully(
        self, timed_client, create_test_product
    ):
        product = create_test_product

        activation_payload = { "status": True }
        activation_response = timed_client.patch(
            f"/api/products/{product.id}/activation",
            activation_payload,
            content_type="application/json",
        )
        assert activation_response.status_code == 200

        activation_body = activation_response.json()
        assert activation_body["id"] == str(product.id)
        assert activation_body["is_active"] is True
        assert_has_valid_timestamps(activation_body)

        deactivation_payload = { "status": False }
        deactivation_response = timed_client.patch(
            f"/api/products/{product.id}/activation",
            deactivation_payload,
            content_type="application/json",
        )
        assert deactivation_response.status_code == 200

        deactivation_body = deactivation_response.json()
        assert deactivation_body["id"] == str(product.id)
        assert deactivation_body["is_active"] is False
        assert_has_valid_timestamps(deactivation_body)

    def test_should_return_404_not_found_for_invalid_product_id(self, timed_client):
        activation_payload = { "status": True }
        activation_response = timed_client.patch(
            f"/api/products/{uuid4()}/activation",
            activation_payload,
            content_type="application/json",
        )
        assert activation_response.status_code == 404
        assert "not found" in activation_response.json()["message"]

@pytest.mark.django_db
class TestDeleteProduct:
    def test_should_return_204_no_content_and_delete_product_successfully(self, create_test_product, timed_client):
        product = create_test_product

        response = timed_client.delete(f"/api/products/{product.id}")

        assert response.status_code == 204

    def test_should_rturn_404_not_found_for_invalid_product_id(self, timed_client):
        response = timed_client.delete(f"/api/products/{uuid4()}")

        assert response.status_code == 404