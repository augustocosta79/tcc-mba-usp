from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from apps.shared.value_objects.email import Email
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.password import Password


class User:
    def __init__(
        self,
        name: Name,
        email: Email,
        password: Password,
        id: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._id = id or uuid4()
        self._name = name
        self._email = email
        self._password = password
        self._username = username or ""
        self._is_active = is_active if is_active is not None else True
        self._created_at = created_at
        self._updated_at = updated_at

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def name(self) -> Name:
        return self._name

    @property
    def email(self) -> Email:
        return self._email
    
    @property
    def password(self) -> Password:
        return self._password

    @property
    def username(self) -> str:
        return self._username

    @property
    def is_active(self) -> bool:
        return self._is_active
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def rename(self, new_name: str) -> None:
        self._name = Name(new_name)

    def change_username(self, new_username: str) -> None:
        self._username = new_username

    def change_password(self, current_raw_password, new_raw_password: str) -> None:
        if self.password.verify(current_raw_password):
            self._password = Password(new_raw_password)

    def activate(self):
        self._is_active = True

    def deactivate(self):
        self._is_active = False
        
