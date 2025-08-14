from uuid import uuid4
from tests.utils.timed_client import TimedClient
import pytest
from apps.users.repository import UserRepository
from apps.users.service import UserService
from apps.addresses.entity import Address
from apps.shared.value_objects.address import Street, StreetNumber, Complement, District, City, StateCode, PostalCode, Country
from apps.addresses.repository import AddressRepository
from utils.logger import configure_logger

address_repository = AddressRepository()
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
def persist_address(test_user):       
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
    return address_repository.save(address)


@pytest.mark.django_db
class TestAddressCreationRoute:
    def test_should_return_status_201_created(self, timed_client, test_user):
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

    def test_should_return_422_unporcessable_entity_error_for_wrong_postal_code(self, timed_client, test_user):
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
    
    def test_should_return_409_conflict_error_for_not_found_user(self, timed_client):
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
    
    def test_should_return_409_conflict_error_for_more_than_one_default_address(self, timed_client, test_user, persist_address):
        persist_address # create a existing default addredd
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


@pytest.mark.django_db
class TestGetAddressByIdRoute:
    def test_should_return_200_ok(self, timed_client, persist_address):
        persisted_address = persist_address
        url = f"/api/addresses/{persisted_address.id}"
        response = timed_client.get(url)
        assert response.status_code == 200

        body = response.json()
        assert body["street"] == persisted_address.street.value
        assert body["street_number"] == persisted_address.street_number.value
        assert body["complement"] == persisted_address.complement.value
        assert body["district"] == persisted_address.district.value
        assert body["city"] == persisted_address.city.value
        assert body["state_code"] == persisted_address.state_code.value
        assert body["postal_code"] == persisted_address.postal_code.value
        assert body["country"] == persisted_address.country.value
        assert body["is_default"] == persisted_address.is_default

    def test_should_return_404_not_found_for_invalid_address_id(self, timed_client):
        url = f"/api/addresses/{uuid4()}"
        response = timed_client.get(url)
        assert response.status_code == 404
        assert "Address not found" in response.json()["message"] 


@pytest.mark.django_db
class TestListAddressesByUser:
    def test_should_return_200_ok(self, timed_client, test_user, persist_address):
        url = f"/api/addresses/user/{test_user.id}"
        persisted_address = persist_address
        response = timed_client.get(url)
        assert response.status_code == 200

        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 1
        assert body[0]["street"] == persisted_address.street.value
        assert body[0]["street_number"] == persisted_address.street_number.value
        assert body[0]["complement"] == persisted_address.complement.value
        assert body[0]["district"] == persisted_address.district.value
        assert body[0]["city"] == persisted_address.city.value
        assert body[0]["state_code"] == persisted_address.state_code.value
        assert body[0]["postal_code"] == persisted_address.postal_code.value
        assert body[0]["country"] == persisted_address.country.value
        assert body[0]["is_default"] == persisted_address.is_default

    def test_should_return_404_for_invalid_user_id(self, timed_client, test_user, persist_address):
        persist_address
        url = f"/api/addresses/user/{uuid4()}"
        response = timed_client.get(url)
        assert response.status_code == 404
        assert "No address associated for this user" in response.json()["message"]

@pytest.mark.django_db
class TestDeleteAddress:
    def test_should_return_204_if_delete_address_or_404_if_not_found(self, timed_client, persist_address):
        persisted_address = persist_address
        url=f"/api/addresses/{persisted_address.id}"
        response_204 = timed_client.delete(url)
        assert response_204.status_code == 204
        assert address_repository.get_address_by_id(persisted_address.id) is None

        response_404 = timed_client.delete(url)
        assert response_404.status_code == 404
        assert "Address not found" in response_404.json()["message"]