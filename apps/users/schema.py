from datetime import datetime
from uuid import UUID

from ninja import Schema


class UserSchema(Schema):
    id: UUID
    email: str
    name: str
    username: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
