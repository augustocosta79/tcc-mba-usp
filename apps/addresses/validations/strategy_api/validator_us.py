from apps.addresses.validations.strategy_api.interface import PostalCodeValidatorInterface
import requests

class UsValidationStrategy(PostalCodeValidatorInterface):
    country_validator = "US"
    
    def create_url(self, postal_code: str, selected_country: str):
        if selected_country != self.country_validator:
            return False
        return f"https://api.zippopotam.us/us/{postal_code}"    
    
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
        url = f"https://api.zippopotam.us/us/{postal_code}"
        response = requests.get(url)
        if response.status_code != 200:
            return False
        data = response.json()
        return (
            data["post code"] == postal_code
            and data["country abbreviation"] == country
            and data["places"][0]["state abbreviation"] == state_code
            and data["places"][0]["place name"].lower() == city.lower()
        )
