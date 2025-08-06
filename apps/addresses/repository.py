from apps.addresses.repository_interface import AddressRepositoryInterface
from apps.addresses.models import AddressModel
from apps.addresses.entity import Address
from apps.addresses.serializers import from_address_model_to_entity
from apps.users.models import UserModel
import pytest


class AddressRepository(AddressRepositoryInterface):
    def save(self, address: Address) -> Address:
        address_model = AddressModel.objects.create(
            user=UserModel.objects.get(id=address.user_id),
            street=address.street.value,
            street_number=address.street_number.value,
            complement=address.complement.value,
            district=address.district.value,
            city=address.city.value,
            state_code=address.state_code.value,
            postal_code=address.postal_code.value,
            country=address.country.value,
            is_default=address.is_default
        )

        return from_address_model_to_entity(address_model)

        
    
    def has_default_address_for(self, user_id) -> bool:
        return AddressModel.objects.filter(user__id=user_id, is_default=True).exists()