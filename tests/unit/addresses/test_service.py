from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from apps.addresses.entity import Address
from apps.addresses.service import AddressService
from apps.shared.value_objects.address import Street, StreetNumber, Complement, District, City, StateCode, PostalCode, Country
from apps.shared.exceptions import UnprocessableEntityError, ConflictError, NotFoundError

mock_repository = MagicMock()
mock_logger = MagicMock()
mock_user = MagicMock()
mock_user_service = MagicMock()
service = AddressService(mock_repository, mock_logger, mock_user_service)

@pytest.fixture
def create_test_address():
    def _create_test_address(
        user_id, street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default
    ):
        street = Street(street_str)
        street_number = StreetNumber(street_number_str)
        complement = Complement(complement_str)
        district = District(district_str)
        city = City(city_str)
        state_code = StateCode(state_code_str)
        postal_code = PostalCode(postal_code_str)
        country = Country(country_str)

        test_address = Address(user_id, street, street_number, complement, district, city,state_code, postal_code, country, is_default)

        return test_address
    return _create_test_address
        

class TestAddressCreation:
    @pytest.mark.parametrize(
        (
            "street_str", "street_number_str", "complement_str", "district_str",
            "city_str", "state_code_str", "postal_code_str", "country_str", "is_default"
        ),
        [
            # valid BR address
            (
                "Rua Humberto de Campos",    # street_str
                "0",                        # street_number_str
                "0",                        # complement_str
                "Leblon",                   # district_str
                "Rio de janeiro",           # city_str
                "RJ",                       # state_code_str
                "22430190",                 # postal_code_str
                "BR",                       # country_str
                True                        # is_default
            ),
            # valid US address
            (
                "1600 Pennsylvania Avenue NW",  # street_str
                "1",                            # street_number_str
                "White House",                  # complement_str
                "Northwest",                    # district_str
                "Washington",                   # city_str
                "DC",                           # state_code_str
                "20500",                        # postal_code_str
                "US",                           # country_str
                True                            # is_default
            )
        ]
    )
    def test_should_create_address_successfully(
        self,
        street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default, create_test_address
    ):
        mock_logger.reset_mock()      
        user_id = mock_user.id

        test_address = create_test_address(user_id, street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default)

        mock_repository.save.return_value = test_address        
        mock_repository.has_default_address_for.return_value = False

        address = service.create_address(
            user_id,
            street_str,
            street_number_str,
            complement_str,
            district_str,
            city_str,
            state_code_str,
            postal_code_str,
            country_str,
            is_default
        )

        assert address.street.value == test_address.street.value
        assert address.street_number.value == test_address.street_number.value
        assert address.complement.value == test_address.complement.value
        assert address.district.value == test_address.district.value
        assert address.city.value == test_address.city.value
        assert address.state_code.value == test_address.state_code.value
        assert address.postal_code.value == test_address.postal_code.value
        assert address.country.value == test_address.country.value
        assert isinstance(address.id, UUID)
        assert address.is_default is True
        mock_logger.info.assert_called_once()
        assert "Address created successfully" in mock_logger.info.call_args[0][0]

    
    @pytest.mark.parametrize(
        (
            "street_str", "street_number_str", "complement_str", "district_str",
            "city_str", "state_code_str", "postal_code_str", "country_str", "is_default"
        ),
        [
            # invalid BR address
            (
                "Rua Humberto de Campos",    # street_str
                "0",                        # street_number_str
                "0",                        # complement_str
                "Leblon",                   # district_str
                "Rio de janeiro",           # city_str
                "RJ",                       # state_code_str
                "22430199",                 # postal_code_str -> wrong number
                "BR",                       # country_str
                True                        # is_default
            ),
            # invalid US address
            (
                "1600 Pennsylvania Avenue NW",  # street_str
                "1",                            # street_number_str
                "White House",                  # complement_str
                "Northwest",                    # district_str
                "Washington",                   # city_str
                "DC",                           # state_code_str
                "90500",                        # postal_code_str -> wrong number
                "US",                           # country_str
                True                            # is_default
            )
        ]
    )
    def test_creation_should_raise_unprocessable_entity_error(
        self,
        street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default
    ):
        mock_logger.reset_mock()      
        user_id = mock_user.id

        street = Street(street_str)
        street_number = StreetNumber(street_number_str)
        complement = Complement(complement_str)
        district = District(district_str)
        city = City(city_str)
        state_code = StateCode(state_code_str)
        postal_code = PostalCode(postal_code_str)
        country = Country(country_str)

        test_address = Address(user_id, street, street_number, complement, district, city,state_code, postal_code, country, is_default)

        mock_repository.save.return_value = test_address

        with pytest.raises(UnprocessableEntityError) as exc:
            service.create_address(
                user_id,
                street_str,
                street_number_str,
                complement_str,
                district_str,
                city_str,
                state_code_str,
                postal_code_str,
                country_str,
                is_default
            )
        assert "Unprocessable address" in str(exc)
        assert mock_logger.warning.called_once()
        assert "Unprocessable address" in mock_logger.warning.call_args[0][0]

    @pytest.mark.parametrize(
        (
            "street_str", "street_number_str", "complement_str", "district_str",
            "city_str", "state_code_str", "postal_code_str", "country_str", "is_default"
        ),
        [
            # valid BR address
            (
                "Rua Humberto de Campos",    # street_str
                "0",                        # street_number_str
                "0",                        # complement_str
                "Leblon",                   # district_str
                "Rio de janeiro",           # city_str
                "RJ",                       # state_code_str
                "22430190",                 # postal_code_str
                "BR",                       # country_str
                True                        # is_default
            )
        ]
    )
    def test_creation_should_raise_conflict_error_for_not_found_user(
        self,
        street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default
    ):
        mock_logger.reset_mock()      
        user_id = mock_user.id

        mock_user_service.get_user_by_id.side_effect = NotFoundError()

        with pytest.raises(ConflictError) as exc:
            service.create_address(
                user_id,
                street_str,
                street_number_str,
                complement_str,
                district_str,
                city_str,
                state_code_str,
                postal_code_str,
                country_str,
                is_default
            )
        assert "address must have a user associated" in str(exc)
        assert mock_logger.warning.called_once()
        assert "address must have a user associated" in mock_logger.warning.call_args[0][0]
        mock_user_service.get_user_by_id.side_effect = None

    @pytest.mark.parametrize(
        (
            "street_str", "street_number_str", "complement_str", "district_str",
            "city_str", "state_code_str", "postal_code_str", "country_str", "is_default"
        ),
        [
            # valid BR address
            (
                "Rua Humberto de Campos",    # street_str
                "0",                        # street_number_str
                "0",                        # complement_str
                "Leblon",                   # district_str
                "Rio de janeiro",           # city_str
                "RJ",                       # state_code_str
                "22430190",                 # postal_code_str
                "BR",                       # country_str
                True                        # is_default
            )
        ]
    )
    def test_creation_should_raise_conflict_error_for_duplicated_default_address(
        self,
        street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default
    ):
        mock_logger.reset_mock()      
        user_id = mock_user.id
        
        mock_user_service.get_user_by_id.return_value = mock_user
        mock_repository.has_default_address_for.return_value = True

        with pytest.raises(ConflictError) as exc:
            service.create_address(
                user_id,
                street_str,
                street_number_str,
                complement_str,
                district_str,
                city_str,
                state_code_str,
                postal_code_str,
                country_str,
                is_default
            )
        assert "one default address per user" in str(exc)
        assert mock_logger.warning.called_once()
        assert "one default address per user" in mock_logger.warning.call_args[0][0]

class TestGetAddressById:
    def test_should_get_address_by_id_successfully(self, create_test_address):
        user_id = mock_user.id
        street_str = "Rua Humberto de Campos"
        street_number_str = "0"
        complement_str = "0"
        district_str = "Leblon"
        city_str = "Rio de janeiro"
        state_code_str = "RJ"
        postal_code_str = "22430190"
        country_str = "BR"
        is_default = True

        test_address = create_test_address(user_id, street_str, street_number_str, complement_str, district_str,
        city_str, state_code_str, postal_code_str, country_str, is_default)

        mock_repository.get_address_by_id.return_value = test_address        
       
        address = service.get_address_by_id(test_address.id)

        assert address.street.value == test_address.street.value
        assert address.street_number.value == test_address.street_number.value
        assert address.complement.value == test_address.complement.value
        assert address.district.value == test_address.district.value
        assert address.city.value == test_address.city.value
        assert address.state_code.value == test_address.state_code.value
        assert address.postal_code.value == test_address.postal_code.value
        assert address.country.value == test_address.country.value
        assert isinstance(address.id, UUID)
        assert address.is_default is True
        mock_logger.info.assert_called_once()
        assert "Address retrieved successfully" in mock_logger.info.call_args[0][0]

    def test_should_raise_not_found_error_for_invalid_address_id(self):
        mock_logger.reset_mock()
        mock_repository.get_address_by_id.return_value = None
        with pytest.raises(NotFoundError) as exc:
            service.get_address_by_id(uuid4())
        assert "Address not found" in str(exc)
        mock_logger.warning.assert_called_once()
        assert "Address not found" in mock_logger.warning.call_args[0][0]

class TestListAddressesForUser:
    def test_should_list_addresses_successfully_for_valid_user_id(self, create_test_address):
        mock_repository.list_addresses_for.return_value = [ create_test_address ]
        addresses = service.list_addresses_for(mock_user.id)
        assert len(addresses) == 1
        mock_logger.info.assert_called_once()
        assert "Address list retrieved successfully" in mock_logger.info.call_args[0][0]
    
    def test_should_raise_not_found_error_for_invalid_user_id(self):
        mock_logger.reset_mock()
        mock_user_service.get_user_by_id.side_effect = NotFoundError("No address associated for this user")
        with pytest.raises(NotFoundError) as exc:
            service.list_addresses_for(uuid4())
        assert "No address associated for this user" in str(exc)
        mock_logger.warning.assert_called_once()
        assert "No address associated for this user" in mock_logger.warning.call_args[0][0]

        mock_user_service.get_user_by_id.side_effect = None

class TestDeleteAddress:
    def test_should_delete_address_successfully(self):
        mock_address = MagicMock()
        mock_repository.get_address_by_id.return_value = mock_address

        service.delete_address(mock_address.id)
        
        mock_repository.delete_address.assert_called_once_with(mock_address.id)
        mock_logger.info.assert_called_once()
        assert "Address deleted successfully" in mock_logger.info.call_args[0][0]
    
    def test_should_raise_not_found_error_for_invalid_address_id(self):
        mock_logger.reset_mock()
        mock_repository.get_address_by_id.return_value = None
        random_id = uuid4()

        with pytest.raises(NotFoundError) as exc:
            service.delete_address(random_id)
        
        assert f"Address not found. Can't find address with id {random_id}" in str(exc)
        mock_logger.warning.assert_called_once()
        assert f"Address not found. Can't find address with id {random_id}" in mock_logger.warning.call_args[0][0]
