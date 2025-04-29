from uuid import UUID
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.models import UserModel
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email

class UserRepository(UserRepositoryInterface):
    def save(self, user: User) -> User:
        created_user_data = UserModel.objects.create(
            id=user.id,
            name=user.name,
            email=user.email,
            username=user.username,
            is_active=user.is_active
        )

        return User(
            id=created_user_data.id,
            name=created_user_data.name,
            email=created_user_data.email,
            username=created_user_data.username,
            is_active=created_user_data.is_active
        )
    
    def get_user_by_id(self, user_id: UUID) -> User:
        user_data = UserModel.objects.get(id=user_id)
        return User(
            id=user_data.id,
            name=user_data.name,
            email=user_data.email,
            username=user_data.username,
            is_active=user_data.is_active
        )
    
    def list_users(self) -> list[User]:
        users_data = UserModel.objects.all()
        users = [
            User(
            id=user_data.id,
            name=Name(user_data.name),
            email=Email(user_data.email),
            username=user_data.username,
            is_active=user_data.is_active
            )
            for user_data in users_data
        ]
        return users