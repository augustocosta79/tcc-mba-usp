from uuid import UUID
from pydantic import BaseModel

class AddressSchema(BaseModel):
    id: UUID
    user_id: UUID
    street: str
    street_number: str
    complement: str
    district: str
    city: str
    state_code: str
    postal_code: str
    country: str
    is_default: bool


class AddressCreateSchema(BaseModel):
    user_id: UUID
    street: str
    street_number: str
    complement: str
    district: str
    city: str
    state_code: str
    postal_code: str
    country: str
    is_default: bool
