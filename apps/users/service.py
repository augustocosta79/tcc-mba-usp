from typing import Optional
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, name: Name, email: str, username: Optional[str] = None) -> User:
        user = User(name=name, email=email, username=username)
        self.repository.save(user)
        return user