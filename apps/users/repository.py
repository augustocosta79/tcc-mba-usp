from uuid import UUID
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.models import UserModel
from apps.users.entity import User
from apps.shared.value_objects import Name, Email, Password


class UserRepository(UserRepositoryInterface):
    def save(self, user: User) -> User:
        created_user_data = UserModel.objects.create(
            id=user.id,
            name=user.name.value,
            email=user.email.value,
            password=user.password.hash,
            username=user.username,
            is_active=user.is_active
        )

        return User(
            id=created_user_data.id,
            name=Name(created_user_data.name),
            email=Email(created_user_data.email),
            password=Password.from_hash(created_user_data.password),
            username=created_user_data.username,
            is_active=created_user_data.is_active,
            created_at=created_user_data.created_at,
            updated_at=created_user_data.updated_at
        )
    
    def update_user(self, user: User) -> User:        
        user_model = UserModel.objects.filter(id=user.id).first()
        if not user_model:
            return None        
        
        user_model.name = user.name.value
        user_model.email = user.email.value
        user_model.password = user.password.hash
        user_model.username = user.username
        user_model.is_active = user.is_active
        user_model.save()
        return User(
            id=user_model.id,
            name=Name(user_model.name),
            email=Email(user_model.email),
            password=Password.from_hash(user_model.password),
            username=user_model.username,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )
    
    def get_user_by_id(self, user_id: UUID) -> User:
        user_data = UserModel.objects.filter(id=user_id).first()
        if not user_data:
            return None
        return User(
            id=user_data.id,
            name=Name(user_data.name),
            email=Email(user_data.email),
            password=Password.from_hash(user_data.password),
            username=user_data.username,
            is_active=user_data.is_active,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at
        )
    
    def list_users(self) -> list[User]:
        users_data = UserModel.objects.all()
        users = [
            User(
            id=user_data.id,
            name=Name(user_data.name),
            email=Email(user_data.email),
            password=Password.from_hash(user_data.password),
            username=user_data.username,
            is_active=user_data.is_active,
            created_at=user_data.created_at,
            updated_at=user_data.updated_at
            )
            for user_data in users_data
        ]
        return users
    
    def delete_user(self, user_id: UUID) -> None:
        UserModel.objects.get(id=user_id).delete()
        return
    
    def get_user_by_email(self, user_email: str) -> User:
        try:
            user_data = UserModel.objects.get(email=user_email)
            return User(
                id=user_data.id,
                name=Name(user_data.name),
                email=Email(user_data.email),
                password=Password.from_hash(user_data.password),
                username=user_data.username,
                is_active=user_data.is_active,
                created_at=user_data.created_at,
                updated_at=user_data.updated_at
            )
        except Exception:
            return None