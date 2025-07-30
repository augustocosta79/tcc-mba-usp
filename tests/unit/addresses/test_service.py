# from unittest.mock import MagicMock

# import pytest
# from apps.addresses.service import AddressService

# mock_repository = MagicMock()
# mock_logger = MagicMock()
# mock_user = MagicMock()
# mock_user_service = MagicMock()
# service = AddressService(mock_repository, mock_logger, mock_user_service)

# mock_user_service.get_user_by_id.return_value = mock_user

# class TestAddress:
#     def test_should_create_address_successfully(self):
        
#         user_id = mock_user.id
#         street = "Rua Humberto de Campos"
#         number = 0
#         complement = 0
#         district = "Leblon"
#         city = "Rio de janeiro"
#         state = "RJ"
#         postal_code = "22430-190"
#         country = "Brasil"
#         is_default = True

#         address = service.create_address(user_id, street, number, complement, district, city, state, postal_code, country, is_default)

#         assert address.street.value == street
#         assert address.number.value == number
#         assert address.complement.value == complement
#         assert address.district.value == district
#         assert address.city.value == city
#         assert address.state.value == state
#         assert address.postal_code.value == postal_code
#         assert address.country.value == country
#         assert address.is_default is True





