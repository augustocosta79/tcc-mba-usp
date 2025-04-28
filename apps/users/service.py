from typing import Optional
from uuid import UUID
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, name: Name, email: Email, username: Optional[str] = None) -> User:
        user = User(name=name, email=email, username=username)
        self.repository.save(user)
        return user
    
    def get_user_by_id(self, user_id: UUID) -> User:
        return self.repository.get_user_by_id(user_id=user_id)
    
    def list_users(self) -> list[User]:
        return self.repository.list_users()