from uuid import uuid4
from tests.utils.timed_client import TimedClient
import pytest
from apps.users.repository import UserRepository
from apps.users.service import UserService
from apps.addresses.entity import Address
from apps.shared.value_objects.address import Street, StreetNumber, Complement, District, City, StateCode, PostalCode, Country
from apps.addresses.repository import AddressRepository
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
def persisted_address(test_user):       
    repository = AddressRepository()
    address = Address(
        user_id=test_user.id,
        street=Street("Rua Humberto de Campos"),
        street_number=StreetNumber("0"),
        complement=Complement("Apt 1"),
        district=District("Leblon"),
        city=City("Rio de Janeiro"),
        state_code=StateCode("RJ"),
        postal_code=PostalCode("22430190"),
        country=Country("BR"),
        is_default=True
    )
    return repository.save(address)


@pytest.mark.django_db
class TestAddressCreationRoute:
    def test_should_respond_status_201_created(self, timed_client, test_user):
        address_payload = {
            "user_id": str(test_user.id),
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

        body = response.json()
        assert body["street"] == address_payload["street"]
        assert body["street_number"] == address_payload["street_number"]
        assert body["complement"] == address_payload["complement"]
        assert body["district"] == address_payload["district"]
        assert body["city"] == address_payload["city"]
        assert body["state_code"] == address_payload["state_code"]
        assert body["postal_code"] == address_payload["postal_code"]
        assert body["country"] == address_payload["country"]
        assert body["is_default"] == address_payload["is_default"]

    def test_should_respond_422_unporcessable_entity_error(self, timed_client, test_user):
        inconsistent_address_payload = {
            "user_id": str(test_user.id),
            "street": "Rua Humberto de Campos",
            "street_number": "0",
            "complement": "Apt 1",
            "district": "Leblon",
            "city": "Rio de Janeiro",
            "state_code": "RJ",
            "postal_code": "22430199", # -> wrong number
            "country": "BR",
            "is_default": True
        }

        url = "/api/addresses"
        response = timed_client.post(url, data=inconsistent_address_payload, content_type="application/json")
        assert response.status_code == 422
        assert "Unprocessable address" in response.json()["message"]
    
    def test_should_respond_409_conflict_error_for_not_found_user(self, timed_client):
        inconsistent_address_payload = {
            "user_id": str(uuid4()), # non existent user id
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
        response = timed_client.post(url, data=inconsistent_address_payload, content_type="application/json")
        assert response.status_code == 409
        assert "address must have a user associated" in response.json()["message"]
    
    def test_should_respond_409_conflict_error_for_more_than_one_default_address(self, timed_client, test_user, persisted_address):
        address_default = persisted_address # create a existing default addredd
        inconsistent_address_payload = {
            "user_id": str(test_user.id),
            "street": "Rua Humberto de Campos",
            "street_number": "0",
            "complement": "Apt 1",
            "district": "Leblon",
            "city": "Rio de Janeiro",
            "state_code": "RJ",
            "postal_code": "22430190",
            "country": "BR",
            "is_default": True # try to make default even already existing one
        }

        url = "/api/addresses"
        response = timed_client.post(url, data=inconsistent_address_payload, content_type="application/json")
        assert response.status_code == 409
        assert "can only be one default address" in response.json()["message"]