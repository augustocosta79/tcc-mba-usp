from abc import ABC, abstractmethod
from uuid import UUID

from apps.addresses.entity import Address

class AddressRepositoryInterface(ABC):
    @abstractmethod
    def save(self, address: Address) -> Address:
        pass

    @abstractmethod
    def has_default_address_for(self, user_id: UUID) -> bool:
        pass

    @abstractmethod
    def get_address_by_id(self, address_id: UUID) -> Address:
        pass

    @abstractmethod
    def list_addresses_for(self, user_id: UUID) -> list[Address]:
        pass

    @abstractmethod
    def delete_address(self, address_id: UUID):
        pass