from uuid import UUID
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.models import UserModel
from apps.users.user_entity import User
from apps.shared.value_objects import Name, Email, Password

from django.core.exceptions import ObjectDoesNotExist

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
            is_active=created_user_data.is_active
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
            is_active=user_model.is_active
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
            is_active=user_data.is_active
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
            is_active=user_data.is_active
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
                is_active=user_data.is_active
            )
        except Exception:
            return None