from apps.addresses.validations.strategy_api.validator_br import BrazilValidationStrategy
from apps.addresses.validations.strategy_api.validator_us import UsValidationStrategy

def get_api_country_strategy(country_code: str):
    strategy = {
        "BR": BrazilValidationStrategy(),
        "US": UsValidationStrategy()
    }
    return strategy.get(country_code)

