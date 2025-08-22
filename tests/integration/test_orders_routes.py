import pytest
from utils.timed_client import TimedClient
from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.products.service import ProductService
from apps.products.repository import ProductRepository
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from apps.addresses.service import AddressService
from apps.addresses.repository import AddressRepository
from apps.carts.service import CartService
from apps.carts.repository import CartRepository
from utils.logger import configure_logger
from apps.orders.enums import OrderStatus

test_logger = configure_logger("orders_test_routes")

user_service = UserService(UserRepository(), test_logger)
product_service = ProductService(ProductRepository(), test_logger)
category_service = CategoryService(CategoryRepository(), test_logger)
address_service = AddressService(AddressRepository(), test_logger)
cart_service = CartService(CartRepository(), product_service, user_service, test_logger)

@pytest.fixture
def timed_client(client):
    return TimedClient(client)

@pytest.mark.django_db
class TestOrderCreation:
    def test_should_return_status_201_created_and_order_data(self, timed_client):        
        user = user_service.create_user("test", "test@mail.com", "Abc@1234")
        category = category_service.create_category("Test Cat", "Test Description")
        product = product_service.create_product("Test Product", "Description", 10.00, 5, user.id, [category.id])
        address = address_service.create_address(
            user.id, "Rua Humberto de Campos", "410", "Apt 101", 
            "Leblon", "Rio de Janeiro", "RJ", 
            "22430190", "BR", True
        )
        
        cart_service.add_to_cart(user.id, product.id, 2)

        url = f"/api/orders/{user.id}"
        
        valid_payload = {
            "address_id": str(address.id)
        }

        response = timed_client.post(
                url, valid_payload, content_type="application/json"
            )
        assert response.status_code == 201

        body = response.json()

        assert body["user"]["id"] == str(user.id)
        assert body["address"]["id"] == str(address.id)
        assert body["status"] == OrderStatus.PENDING.value
        assert len(body["items"]) == 1
        assert body["items"][0]["quantity"] == 2
