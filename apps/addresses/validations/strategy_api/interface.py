from abc import ABC, abstractmethod


class PostalCodeValidatorInterface(ABC):
    @abstractmethod
    def create_url(self, postal_code: str, country: str):
        pass

    @abstractmethod
    def validate(
        street: str,
        street_number: str,
        complement: str,
        district: str,
        city: str,
        state_code: str,
        postal_code: str,
        country: str,
    ):
        pass