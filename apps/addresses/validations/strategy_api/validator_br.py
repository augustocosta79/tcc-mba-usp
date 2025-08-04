from apps.addresses.validations.strategy_api.interface import PostalCodeValidatorInterface
import requests

class BrazilValidationStrategy(PostalCodeValidatorInterface):
    country_validator = "BR"

    def create_url(self, postal_code:str, selected_country:str):
        if selected_country != self.country_validator:
            return False
        return f"https://brasilapi.com.br/api/cep/v1/{postal_code}"
    
    def validate(
        self,
        street,
        street_number,
        complement,
        district,
        city,
        state_code,
        postal_code,
        country,
    ):
        data = None
        url = f"https://brasilapi.com.br/api/cep/v1/{postal_code}"
        response = requests.get(url)
        if response.status_code != 200:
            return False
        data = response.json()
        return (
            data["cep"] == postal_code
            and data["state"] == state_code
            and data["city"].lower() == city.lower()
            and data["street"].lower() == street.lower()
            and data["neighborhood"].lower() == district.lower()
        )
