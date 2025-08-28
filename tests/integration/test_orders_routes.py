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
def get_product_by_id(timed_client):
    def _get_product(id):
        response = timed_client.get(f"/api/products/{id}")
        assert response.status_code == 200
        return response.json()
    return _get_product

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


@pytest.fixture
def request_order_creation(timed_client, create_test_product, add_test_product_to_cart):
    def _create(test_user, test_address, product_stock, item_quantity):
        user_id = test_user["id"]
        address_id = test_address["id"]
        product = create_test_product(product_stock)       
        add_test_product_to_cart(product, item_quantity)

        url = f"/api/orders/users/{user_id}"
        
        valid_payload = {
            "address_id": address_id
        }

        response = timed_client.post(
                url, valid_payload, content_type="application/json"
            )
        assert response.status_code == 201

        return response
    return _create


def assert_order_created_successfully(body, user_dict, address_dict, item_quantity):
    assert body["user"]["id"] == str(user_dict["id"])
    assert body["address"]["id"] == str(address_dict["id"])
    assert body["status"] == OrderStatus.PENDING.value
    assert len(body["items"]) == 1
    assert body["items"][0]["quantity"] == item_quantity

def assert_order_data_is_equal(body, creation_body, product_stock, item_quantity):
    assert body["id"] == creation_body["id"]
    assert body["user"]["id"] == creation_body["user"]["id"]
    assert body["address"]["id"] == creation_body["address"]["id"]
    assert len(body["items"]) == len(creation_body["items"])
    assert body["items"][0]["product"]["id"] == creation_body["items"][0]["product"]["id"]
    assert body["items"][0]["product"]["stock"] == product_stock - item_quantity
    assert body["items"][0]["quantity"] == item_quantity
    assert body["items"][0]["price"] == creation_body["items"][0]["price"]


@pytest.mark.django_db
class TestOrderCreation:
    def test_should_return_status_201_created_and_order_data(self, test_user, test_address, request_order_creation):
        product_stock = 10
        item_quantity = 3
        response = request_order_creation(test_user, test_address, product_stock, item_quantity)

        body = response.json()
        assert_order_created_successfully(body, test_user, test_address, item_quantity)
        assert body["items"][0]["product"]["stock"] == product_stock - item_quantity


@pytest.mark.django_db
class TestGetOrderById:
    def test_should_return_status_200_ok_and_order_data_by_id(self, timed_client, test_user, test_address, request_order_creation):
        product_stock = 10
        item_quantity = 3
        creation_response = request_order_creation(test_user, test_address, product_stock, item_quantity)

        creation_body = creation_response.json()
        assert_order_created_successfully(creation_body, test_user,test_address, item_quantity)

        order_id = creation_body["id"]
        url = f"/api/orders/{order_id}"

        response = timed_client.get(url)
        assert response.status_code == 200

        body = response.json()
        assert_order_data_is_equal(body, creation_body, product_stock, item_quantity)
        assert body["status"] == creation_body["status"]


@pytest.mark.django_db
class TestListOrdersByUserId:
    def test_should_return_status_200_ok_and_list_orders_by_user_id(self, timed_client, test_user, test_address, request_order_creation):
        product_stock = 10
        item_quantity = 3
        creation_response = request_order_creation(test_user, test_address, product_stock, item_quantity)

        creation_body = creation_response.json()
        assert_order_created_successfully(creation_body, test_user,test_address, item_quantity)

        url = "/api/orders"
        response = timed_client.get(url, data={"user_id": str(test_user["id"])})

        assert response.status_code == 200
        body = response.json()

        assert len(body) == 1
        assert_order_data_is_equal(body[0], creation_body, product_stock, item_quantity)
        assert body[0]["status"] == creation_body["status"]


@pytest.mark.django_db
class TestOrdersStatusChange:
    def test_should_return_status_200_ok_and_change_order_status_from_pending_to_approved(self, timed_client, test_user, test_address, request_order_creation):
        product_stock = 10
        item_quantity = 3
        creation_response = request_order_creation(test_user, test_address, product_stock, item_quantity)

        creation_body = creation_response.json()
        assert_order_created_successfully(creation_body, test_user,test_address, item_quantity)

        order_id = creation_body["id"]
        payload = { "new_status": "approved" }
        url = f"/api/orders/{order_id}/status"
        response = timed_client.patch(
            url, payload, content_type="application/json"
        )

        assert response.status_code == 200
        body = response.json()
        assert_order_data_is_equal(body, creation_body, product_stock, item_quantity)
        assert body["status"] == payload["new_status"]


@pytest.mark.django_db
class TestRemoveOrderItem:
    def test_should_return_status_200_ok_and_remove_order_by_item_id(self, timed_client, test_user, test_address, request_order_creation, create_test_product, add_test_product_to_cart, get_product_by_id):
        product2_stock = 4
        item2_quantity = 2
        product2_data = create_test_product(product2_stock)
        add_test_product_to_cart(product2_data, item2_quantity)
        assert product2_data["stock"] == product2_stock

        product1_stock = 10
        item1_quantity = 3
        creation_response = request_order_creation(test_user, test_address, product1_stock, item1_quantity)
        creation_body = creation_response.json()

        assert len(creation_body["items"]) == 2

        order_item2_data = creation_body["items"][0]
        order_item1_data = creation_body["items"][1]

        assert order_item2_data["product"]["id"] == product2_data["id"]
        assert order_item2_data["product"]["stock"] == product2_stock - item2_quantity
        assert order_item1_data["product"]["stock"] == product1_stock - item1_quantity

        order_id = creation_body["id"]

        item_to_remove_id = order_item2_data["id"]
        
        url = f"/api/orders/{order_id}/items/{item_to_remove_id}"

        response = timed_client.delete(url)
        assert response.status_code == 200
        result_body = response.json()

        assert result_body["id"] == creation_body["id"]
        assert len(result_body["items"]) == 1
        assert result_body["items"][0]["id"] == order_item1_data["id"]

        check_product_id = order_item2_data["product"]["id"]
        released_stock_product = get_product_by_id(check_product_id)
        assert released_stock_product["id"] == product2_data["id"]
        assert released_stock_product["stock"] == product2_stock

@pytest.mark.django_db
class TestCancelOrder:
    def test_should_return_status_200_ok_cancel_order_and_release_stock(self, timed_client, test_user, test_address, request_order_creation):
        product_stock = 10
        item_quantity = 3
        creation_response = request_order_creation(test_user, test_address, product_stock, item_quantity)

        creation_body = creation_response.json()
        assert_order_created_successfully(creation_body, test_user, test_address, item_quantity)
        assert creation_body["items"][0]["product"]["stock"] == product_stock - item_quantity
        assert creation_body["status"] == OrderStatus.PENDING.value

        order_id = creation_body["id"]
        url = f"/api/orders/{order_id}/cancel"
        response = timed_client.patch(url)
        assert response.status_code == 200
        
        body = response.json()
        assert body["id"] == creation_body["id"]
        assert body["status"] == OrderStatus.CANCELED.value
        body_item = body["items"][0]
        assert body_item["product"]["id"] == creation_body["items"][0]["product"]["id"]
        assert body_item["product"]["stock"] == product_stock
