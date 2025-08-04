from apps.addresses.validations.strategy_api.factory import get_api_country_strategy
from apps.addresses.validations.strategy_api.interface import PostalCodeValidatorInterface


def validate_postal_code(
    street: str,
    street_number: str,
    complement: str,
    district: str,
    city: str,
    state_code: str,
    postal_code: str,
    country: str,
):
    validator: PostalCodeValidatorInterface = get_api_country_strategy(country)
    if not validator:
        print("validator aquisition error")
        return True # do not stop api if country has no strategy
    return validator.validate(
        street,
        street_number,
        complement,
        district,
        city,
        state_code,
        postal_code,
        country,
    )