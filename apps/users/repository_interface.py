from abc import ABC, abstractmethod
from uuid import UUID
from apps.users.entity import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(self,user: User) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    def list_users(self) -> list[User]:
        pass

    @abstractmethod
    def delete_user(self) -> None:
        pass

    @abstractmethod
    def get_user_by_email(self) -> User:
        pass