from logging import Logger
from uuid import UUID

from apps.addresses.entity import Address
from apps.addresses.repository_interface import AddressRepositoryInterface
from apps.shared.value_objects import (
    City,
    Complement,
    Country,
    District,
    StreetNumber,
    PostalCode,
    StateCode,
    Street
)
from apps.users.repository import UserRepository
from apps.users.service import UserService
from utils.logger import configure_logger
from apps.addresses.validations.validators import validate_postal_code
from apps.shared.exceptions import UnprocessableEntityError, NotFoundError, ConflictError

logger = configure_logger(__name__)


class AddressService:
    def __init__(
        self,
        repository: AddressRepositoryInterface,
        logger: Logger,
        user_service: UserService = None,
    ):
        self.repository = repository
        self.logger = logger
        self.user_service = user_service or UserService(UserRepository(), logger)

    def create_address(
        self,
        user_id: UUID,
        street_str: str,
        street_number_value: str,
        complement_str: str,
        district_str: str,
        city_str: str,
        state_code_str: str,
        postal_code_str: str,
        country_str: str,
        is_default: bool,
    ) -> Address:
        street = Street(street_str)
        street_number = StreetNumber(street_number_value)
        complement = Complement(complement_str)
        district = District(district_str)
        city = City(city_str)
        state_code = StateCode(state_code_str)
        postal_code = PostalCode(postal_code_str)
        country = Country(country_str)

        is_valid_address_data = validate_postal_code(
            street.value,
            street_number.value,
            complement.value,
            district.value,
            city.value,
            state_code.value,
            postal_code.value,
            country.value,
        )

        if not is_valid_address_data:
            self.logger.warning("Unprocessable address. The address data does not match the postal code.")
            raise UnprocessableEntityError("Unprocessable address. The address data does not match the postal code.")
        
        try:
            user = self.user_service.get_user_by_id(user_id)
        except NotFoundError:
            self.logger.warning("Each address must have a user associated.")
            raise ConflictError("Each address must have a user associated.")

        if is_default and self.repository.has_default_address_for(user_id):
            self.logger.warning("There can only be one default address per user")
            raise ConflictError("There can only be one default address per user")

        address = Address(
            user_id=user.id,
            street=street,
            street_number=street_number,
            complement=complement,
            district=district,
            city=city,
            state_code=state_code,
            postal_code=postal_code,
            country=country,
            is_default=is_default,
        )

        saved_address = self.repository.save(address)
        self.logger.info(f"Address created successfully: {saved_address}")
        return saved_address
    
    def get_address_by_id(self, address_id: UUID) -> Address:
        if not (address:=self.repository.get_address_by_id(address_id)):
            self.logger.warning(f"Address not found. Can't find address with id {address_id}")
            raise NotFoundError(f"Address not found. Can't find address with id {address_id}")
        self.logger.info("Address retrieved successfully")
        return address
    
    def list_addresses_for(self, user_id: UUID):
        try:
            user = self.user_service.get_user_by_id(user_id)
        except NotFoundError:
            self.logger.warning("No address associated for this user.")
            raise NotFoundError("No address associated for this user.")

        self.logger.info("Address list retrieved successfully")
        return self.repository.list_addresses_for(user.id)
    
    def delete_address(self, address_id: UUID):
        address = self.repository.get_address_by_id(address_id)
        if not address:
            self.logger.warning(f"Address not found. Can't find address with id {address_id}")
            raise NotFoundError(f"Address not found. Can't find address with id {address_id}")
        self.repository.delete_address(address.id)
        self.logger.info("Address deleted successfully")
        return