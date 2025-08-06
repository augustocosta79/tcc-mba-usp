from abc import ABC, abstractmethod
from uuid import UUID

from apps.addresses.entity import Address

class AddressRepositoryInterface(ABC):
    @abstractmethod
    def save(address: Address) -> Address:
        pass

    @abstractmethod
    def has_default_address_for(user_id: UUID) -> bool:
        pass