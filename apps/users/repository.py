from uuid import UUID
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.models import UserModel
from apps.users.user_entity import User

class UserRepository(UserRepositoryInterface):
    def save(self, user: User) -> User:
        return UserModel.objects.create(
            id=user.id,
            name=user.name,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    def get_user_by_id(self, user_id: UUID) -> User:
        return UserModel.objects.get(id=user_id)
    
    def list_users(self) -> list[User]:
        return UserModel.objects.all()