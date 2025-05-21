from typing import Optional
from uuid import UUID

from apps.shared.value_objects.email import EMAIL_REGEX

from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: UUID
    email: str
    name: str
    username: str
    is_active: bool

class UserCreateSchema(BaseModel):
    name: str = Field(..., min_length=2)
    email: str = Field(..., pattern=EMAIL_REGEX)
    username: Optional[str] = ""
    password: str = Field(...,min_length=8)



class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    username: Optional[str] = None


class UserActivationSchema(BaseModel):
    status: bool



class UserPasswordSchema(BaseModel):
    current_password: str
    new_password: str