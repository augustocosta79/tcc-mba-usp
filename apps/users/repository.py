from apps.users.repository_interface import UserRepositoryInterface
from apps.users.user_entity import User

class UserRepository(UserRepositoryInterface):
    def save(user: User) -> User:
        print("user saved")
        return