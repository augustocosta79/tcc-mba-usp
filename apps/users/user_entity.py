from typing import Optional
from uuid import UUID, uuid4

from apps.shared.value_objects.email import Email
from apps.shared.value_objects.name import Name


class User:
    def __init__(
        self,
        name: Name,
        email: Email,
        id: Optional[str] = None,
        username: Optional[str] = None,
        is_active: Optional[bool] = None,
    ):
        self._id = id or uuid4()
        self._name = name
        self._email = email
        self._username = username or ""
        self._is_active = is_active or True

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
    def username(self) -> str:
        return self._username

    @property
    def is_active(self) -> bool:
        return self._is_active

    def rename(self, new_name: Name) -> None:
        self._name = Name(new_name)

    def change_username(self, new_username: str) -> None:
        self._username = new_username
