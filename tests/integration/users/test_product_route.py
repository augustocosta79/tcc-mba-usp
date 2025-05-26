from uuid import UUID, uuid4
from datetime import datetime
from apps.products.service import ProductService
from apps.products.repository import ProductRepository
from apps.shared.value_objects import Title, Description, Price, Stock
import json
import pytest

@pytest.fixture
def create_product_parameters():
    title_string = "valid Title"
    title = Title(title_string)

    description_string = "valid desctiprion"
    description = Description(description_string)

    price_value = "1.99"
    price = Price(price_value)

    stock_value = 5
    stock = Stock(stock_value)

    owner_id = uuid4()

    return title, description, price, stock, owner_id


@pytest.fixture
def create_test_product(create_product_parameters):
    repository = ProductRepository()
    service = ProductService(repository)

    title, description, price, stock, owner_id = create_product_parameters
    
    product = service.create_product(title, description, price, stock, owner_id)

    return product


@pytest.mark.django_db
class TestCreateProduct:
    def test_should_create_product_successfully(self, client):
        valid_payload = {
            "title": "valid Title",
            "description": "valid description",
            "price": "1.99",
            "stock": 3,
            "owner_id": str(uuid4()),
        }

        response = client.post(
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
        assert "created_at" in body
        assert "updated_at" in body
        created_at = body["created_at"]
        updated_at = body["updated_at"]
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        assert isinstance(datetime.strptime(created_at, date_format), datetime)
        assert isinstance(datetime.strptime(updated_at, date_format), datetime)


@pytest.mark.django_db
class TestGetProductbyId:
    def test_should_get_product_by_id_successfully(self, client, create_test_product):
        existing_product = create_test_product

        response = client.get(f"/api/products/{existing_product.id}")
        
        assert response.status_code == 200

        retrived_product = response.json()

        assert retrived_product["id"] == str(existing_product.id)
        assert retrived_product["title"] == existing_product.title.text
        assert retrived_product["description"] == existing_product.description.text
        assert retrived_product["price"] == str(existing_product.price.value)
        assert retrived_product["stock"] == existing_product.stock.value
        assert retrived_product["owner_id"] == str(existing_product.owner_id)