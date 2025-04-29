from typing import Optional
from uuid import UUID

from apps.shared.value_objects.email import Email
from apps.shared.value_objects.name import Name
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.schema import UserUpdateSchema
from apps.users.user_entity import User


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(
        self, name: Name, email: Email, username: Optional[str] = None
    ) -> User:
        user = User(name=name, email=email, username=username)
        self.repository.save(user)
        return user

    def get_user_by_id(self, user_id: UUID) -> User:
        return self.repository.get_user_by_id(user_id=user_id)

    def list_users(self) -> list[User]:
        return self.repository.list_users()

    def update_user(self, user_id: UUID, payload: UserUpdateSchema):
        user = self.repository.get_user_by_id(user_id=user_id)

        operations = {"name": user.rename, "username": user.change_username}

        for attr, value in payload.items():
            operations[attr](value)

        self.repository.save(user)
