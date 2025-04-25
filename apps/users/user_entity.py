from datetime import datetime
from typing import Optional
from uuid import uuid4
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email

class User:
    name: Name
    email: Email
    username: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool

    def __init__(self, name: Name, email: Email, username: Optional[str]):
        self.name = name
        self.email = email
        self.username = username
        self.is_active = True
        self.created_at = datetime.now()
        self.updated_at = datetime.now()