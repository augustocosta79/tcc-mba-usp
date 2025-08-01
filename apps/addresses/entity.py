from typing import Optional
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

from uuid import UUID, uuid4


class Address:
    def __init__(
        self,
        user_id: UUID,
        street: Street,
        street_number: StreetNumber,
        complement: Complement,
        district: District,
        city: City,
        state_code: StateCode,
        postal_code: PostalCode,
        country: Country,
        is_default: bool,
        id: Optional[UUID] = None
    ):
        self._user_id = user_id
        self._street = street
        self._street_number = street_number
        self._complement = complement
        self._district = district
        self._city = city
        self._state_code = state_code
        self._postal_code = postal_code
        self._country = country
        self._is_default = is_default
        self._id = id or uuid4()

    @property
    def id(self) -> UUID:
        return self._id
    
    @property
    def user_id(self) -> UUID:
        return self._user_id
    
    @property
    def street(self) -> Street:
        return self._street
    
    @property
    def street_number(self) -> StreetNumber:
        return self._street_number
    
    @property
    def complement(self) -> Complement:
        return self._complement
    
    @property
    def district(self) -> District:
        return self._district
    
    @property
    def city(self) -> City:
        return self._city
    
    @property
    def state_code(self) -> StateCode:
        return self._state_code
    
    @property
    def postal_code(self) -> PostalCode:
        return self._postal_code
    
    @property
    def country(self) -> Country:
        return self._country
    
    @property
    def is_default(self) -> bool:
        return self._is_default
    
        
