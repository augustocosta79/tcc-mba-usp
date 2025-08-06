from uuid import UUID, uuid4
from apps.addresses.entity import Address
from apps.shared.value_objects.address import Street, StreetNumber, Complement, District, City, StateCode, PostalCode, Country
from apps.addresses.repository import AddressRepository
from utils.logger import configure_logger
from apps.users.repository import UserRepository
from apps.users.service import UserService
import pytest

repository = AddressRepository()

user_id = uuid4()
street_str = "Rua Humberto de Campos"
street_number_str = "0"
complement_str = "0"
district_str = "Leblon"
city_str = "Rio de janeiro"
state_code_str = "RJ"
postal_code_str = "22430190"
country_str = "BR"
is_default = True

street = Street(street_str)
street_number = StreetNumber(street_number_str)
complement = Complement(complement_str)
district = District(district_str)
city = City(city_str)
state_code = StateCode(state_code_str)
postal_code = PostalCode(postal_code_str)
country = Country(country_str)

@pytest.fixture
def test_user():
    logger = configure_logger(__name__)
    repository = UserRepository()
    service = UserService(repository, logger)
    user = service.create_user("test user", "email@test.com", "Abc@1234", "usernameTest")
    return user

@pytest.fixture
def get_saved_address(test_user):
    address = Address(
        user_id=test_user.id,
        street=street,
        street_number=street_number,
        complement=complement,
        district=district,
        city=city,
        state_code=state_code,
        postal_code=postal_code,
        country=country,
        is_default=is_default
    )

    return repository.save(address)


@pytest.mark.django_db
class TestAddressCreation:
    def test_repository_should_save_address_successfully(self, test_user, get_saved_address):
        saved_address = get_saved_address
        
        assert saved_address is not None
        assert saved_address.street == street
        assert saved_address.street_number == street_number
        assert saved_address.complement == complement
        assert saved_address.district == district
        assert saved_address.city == city
        assert saved_address.state_code == state_code
        assert saved_address.postal_code == postal_code
        assert saved_address.country == country
        assert saved_address.is_default == is_default
        assert saved_address.user_id == test_user.id

    def test_repository_should_return_true_if_user_id_has_more_than_one_default_address(self, test_user):
        address1 = Address(
            user_id=test_user.id,
            street=street,
            street_number=street_number,
            complement=complement,
            district=district,
            city=city,
            state_code=state_code,
            postal_code=postal_code,
            country=country,
            is_default=False
        )

        repository.save(address1)

        assert repository.has_default_address_for(test_user.id) is False
        
        address2 = Address(
            user_id=test_user.id,
            street=street,
            street_number=street_number,
            complement=complement,
            district=district,
            city=city,
            state_code=state_code,
            postal_code=postal_code,
            country=country,
            is_default=True
        )

        repository.save(address2)

        assert repository.has_default_address_for(test_user.id) is True

@pytest.mark.django_db
class TestGetAddressById:
    def test_should_return_address_by_id_successfully_for_valid_address_id(self, get_saved_address):
        saved_address = get_saved_address
        address = repository.get_address_by_id(saved_address.id)

        assert saved_address.id == address.id
        assert saved_address.street == address.street
        assert saved_address.street_number == address.street_number
        assert saved_address.complement == address.complement
        assert saved_address.district == address.district
        assert saved_address.city == address.city
        assert saved_address.state_code == address.state_code
        assert saved_address.postal_code == address.postal_code
        assert saved_address.country == address.country
        assert saved_address.is_default == address.is_default
        assert saved_address.user_id == address.user_id

    def test_should_return_None_for_invalid_address_id(self):
        assert repository.get_address_by_id(uuid4()) is None


@pytest.mark.django_db
class TestListAddressesForUser:
    def test_should_get_user_addresses_for_valid_user_successfully(self, test_user, get_saved_address):
        address = get_saved_address
        addresses = repository.list_addresses_for(test_user.id)
        assert len(addresses) == 1

        saved_address = addresses[0]

        assert saved_address.id == address.id
        assert saved_address.street == address.street
        assert saved_address.street_number == address.street_number
        assert saved_address.complement == address.complement
        assert saved_address.district == address.district
        assert saved_address.city == address.city
        assert saved_address.state_code == address.state_code
        assert saved_address.postal_code == address.postal_code
        assert saved_address.country == address.country
        assert saved_address.is_default == address.is_default
        assert saved_address.user_id == address.user_id

@pytest.mark.django_db
class TestDeleteAddress:
    def test_should_delete_address_sccessfully(self, get_saved_address):
        saved_address = get_saved_address
        repository.delete_address(saved_address.id)
        deleted_address = repository.get_address_by_id(saved_address.id)
        assert deleted_address is None
