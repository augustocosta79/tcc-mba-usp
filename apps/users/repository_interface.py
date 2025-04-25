from abc import ABC, abstractmethod
from apps.users.user_entity import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def save(user: User) -> User:
        pass