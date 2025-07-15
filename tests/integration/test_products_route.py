from datetime import datetime
from uuid import UUID, uuid4

import pytest
from apps.products.repository import ProductRepository
from apps.products.service import ProductService
from tests.utils.timed_client import TimedClient

from tests.utils.assertions import assert_has_valid_timestamps

from utils.logger import configure_logger


@pytest.fixture
def timed_client(client):
    return TimedClient(client)


@pytest.fixture
def create_product_parameters():
    title = "valid Title"
    description = "valid desctiprion"
    price = "1.99"
    stock = 5
    owner_id = uuid4()

    category = "test"

    return title, description, price, stock, owner_id, category


@pytest.fixture
def create_test_product(create_product_parameters):
    repository = ProductRepository()
    logger = configure_logger(__name__)
    service = ProductService(repository, logger)

    title, description, price, stock, owner_id, category = create_product_parameters

    product = service.create_product(
        title, description, price, stock, owner_id, category
    )

    return product


@pytest.mark.django_db
class TestCreateProduct:
    def test_should_create_product_successfully(self, timed_client):
        valid_payload = {
            "title": "valid Title",
            "description": "valid description",
            "price": "1.99",
            "stock": 3,
            "owner_id": str(uuid4()),
            "category": "test",
        }

        response = timed_client.post(
            "/api/products", valid_payload, content_type="application/json"
        )
        assert response.status_code == 201

        body = response.json()

        assert "id" in body
        assert isinstance(UUID(body["id"]), UUID)
        assert body["title"] == valid_payload["title"]
        assert body["description"] == valid_payload["description"]
        assert body["price"] == valid_payload["price"]
        assert body["stock"] == valid_payload["stock"]
        assert body["owner_id"] == valid_payload["owner_id"]
        assert body["category"] == valid_payload["category"]
        assert "created_at" in body
        assert "updated_at" in body
        assert_has_valid_timestamps(body)


@pytest.mark.django_db
class TestGetProductbyId:
    def test_should_get_product_by_id_successfully(
        self, timed_client, create_test_product
    ):
        existing_product = create_test_product

        response = timed_client.get(f"/api/products/{existing_product.id}")

        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(existing_product.id)
        assert body["title"] == existing_product.title.text
        assert body["description"] == existing_product.description.text
        assert body["price"] == str(existing_product.price.value)
        assert body["stock"] == existing_product.stock.value
        assert body["owner_id"] == str(existing_product.owner_id)
        assert body["category"] == existing_product.category
        assert body["is_active"] is existing_product.is_active
        assert_has_valid_timestamps(body)


@pytest.mark.django_db
class TestGetProductByCategory:
    def test_should_list_products_by_category_successfully(
        self, timed_client, create_test_product
    ):
        product = create_test_product

        response = timed_client.get("/api/products", {"category": product.category})
        assert response.status_code == 200

        body = response.json()

        assert isinstance(body, list)
        assert len(body) == 1
        assert body[0]["id"] == str(product.id)
        assert body[0]["category"] == product.category
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
    def test_should_update_product_data_successfully(
        self, timed_client, create_test_product, send_update_request
    ):
        product = create_test_product

        title_payload = {"title": "changed title"}
        body = send_update_request(timed_client, product.id, title_payload)

        assert body["id"] == str(product.id)
        assert body["title"] == title_payload["title"]
        assert body["description"] == product.description.text
        assert body["price"] == str(product.price.value)
        assert body["stock"] == product.stock.value
        assert body["owner_id"] == str(product.owner_id)
        assert body["category"] == product.category
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

        category_payload = {"category": f"{str(uuid4())}"}
        body = send_update_request(timed_client, product.id, category_payload)
        assert body["category"] == category_payload["category"]


@pytest.mark.django_db
class TestProductActivation:
    def test_should_activate_product_successfully(
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

@pytest.mark.django_db
class TestDeleteProduct:
    def test_should_delete_product_successfully(self, create_test_product, timed_client):
        product = create_test_product

        response = timed_client.delete(f"/api/products/{product.id}")

        assert response.status_code == 204

    def test_should_get_404_response_for_invalid_product_id(self, timed_client):
        response = timed_client.delete(f"/api/products/{uuid4()}")

        assert response.status_code == 404