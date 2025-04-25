from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email

class User:
    def __init__(self, name: Name, email: Email, username: Optional[str]):
        self._id = uuid4()
        self._name = name
        self._email = email
        self._username = username
        self._is_active = True
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

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
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at