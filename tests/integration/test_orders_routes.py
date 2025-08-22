import json
import pytest
from tests.utils.timed_client import TimedClient
from apps.orders.enums import OrderStatus


@pytest.fixture
def timed_client(client):
    return TimedClient(client)


@pytest.fixture
def test_user(timed_client):
    payload = {
            "name": "Augusto",
            "email": "test@email.com",
            "username": "augustocosta",
            "password": "Abc@1234",
        }

    response = timed_client.post(
        "/api/users", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 201
    return response.json()

@pytest.fixture
def test_category(timed_client):
    url = "/api/categories"
    payload = {
        "name": "Category",
        "description": "cat description"
    }
    response = timed_client.post(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def test_address(timed_client, test_user):
    address_payload = {
        "user_id": test_user["id"],
        "street": "Rua Humberto de Campos",
        "street_number": "0",
        "complement": "Apt 1",
        "district": "Leblon",
        "city": "Rio de Janeiro",
        "state_code": "RJ",
        "postal_code": "22430190",
        "country": "BR",
        "is_default": True
    }

    url = "/api/addresses"
    response = timed_client.post(url, data=address_payload, content_type="application/json")
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def create_test_product(timed_client, test_user, test_category):
    def _create(stock):
        product_payload = {
            "title": "valid Title",
            "description": "valid description",
            "price": "1.99",
            "stock": stock,
            "owner_id": test_user["id"],
            "categories": [ test_category["id"] ],
        }

        product_response = timed_client.post(
            "/api/products", product_payload, content_type="application/json"
        )
        assert product_response.status_code == 201
        return product_response.json()
    return _create

@pytest.fixture
def add_test_product_to_cart(timed_client, test_user):
    def _add(product, quantity):
        user_id = test_user["id"]
        url = f"/api/carts/{user_id}/add"
        payload = {
            "product_id": product["id"],
            "quantity": quantity
        }

        response = timed_client.post(url, data=json.dumps(payload), content_type="application/json")
        assert response.status_code == 200
        return response.json()
    return _add


@pytest.mark.django_db
class TestOrderCreation:
    def test_should_return_status_201_created_and_order_data(self, timed_client, create_test_product, test_user, test_address, add_test_product_to_cart):
        user_id = test_user["id"]
        address_id = test_address["id"]
        product = create_test_product(10)       
        add_test_product_to_cart(product, 3)

        url = f"/api/orders/{user_id}"
        
        valid_payload = {
            "address_id": address_id
        }

        response = timed_client.post(
                url, valid_payload, content_type="application/json"
            )
        assert response.status_code == 201

        body = response.json()

        assert body["user"]["id"] == str(user_id)
        assert body["address"]["id"] == str(address_id)
        assert body["status"] == OrderStatus.PENDING.value
        assert len(body["items"]) == 1
        assert body["items"][0]["quantity"] == 3
