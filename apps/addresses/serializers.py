from apps.addresses.entity import Address
from apps.addresses.models import AddressModel
from apps.shared.value_objects.address import (
    City,
    Complement,
    Country,
    District,
    PostalCode,
    StateCode,
    Street,
    StreetNumber,
)
from apps.addresses.schema import AddressSchema


def from_address_model_to_entity(address_model: AddressModel) -> Address:
    return Address(
        address_model.user.id,
        Street(address_model.street),
        StreetNumber(address_model.street_number),
        Complement(address_model.complement),
        District(address_model.district),
        City(address_model.city),
        StateCode(address_model.state_code),
        PostalCode(address_model.postal_code),
        Country(address_model.country),
        address_model.is_default,
        address_model.id,
    )

def from_address_entity_to_schema(address: Address) -> AddressSchema:
    return AddressSchema(
        id=address.id,
        user_id=address.user_id,
        street=address.street.value,
        street_number=address.street_number.value,
        complement=address.complement.value,
        district=address.district.value,
        city=address.city.value,
        state_code=address.state_code.value,
        postal_code=address.postal_code.value,
        country=address.country.value,
        is_default=address.is_default,
    )

