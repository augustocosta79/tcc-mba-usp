from typing import Optional
from uuid import UUID

from ninja import Schema


class UserSchema(Schema):
    id: UUID
    email: str
    name: str
    username: str
    is_active: bool


class UserUpdateSchema(Schema):
    name: Optional[str]
    username: Optional[str]
