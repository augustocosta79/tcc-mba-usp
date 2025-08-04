from unittest.mock import MagicMock
from uuid import UUID

import pytest
from apps.addresses.entity import Address
from apps.addresses.service import AddressService
from apps.shared.value_objects.address import Street, StreetNumber, Complement, District, City, StateCode, PostalCode, Country
from apps.shared.exceptions import UnprocessableEntityError

mock_repository = MagicMock()
mock_logger = MagicMock()
mock_user = MagicMock()
mock_user_service = MagicMock()
service = AddressService(mock_repository, mock_logger, mock_user_service)

mock_user_service.get_user_by_id.return_value = mock_user

class TestAddress:
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

        assert address.street.value == street.value
        assert address.street_number.value == street_number.value
        assert address.complement.value == complement.value
        assert address.district.value == district.value
        assert address.city.value == city.value
        assert address.state_code.value == state_code.value
        assert address.postal_code.value == postal_code.value
        assert address.country.value == country.value
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
            # valid BR address
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
            # valid US address
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
    def test_should_raise_unprocessable_entity_error(
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