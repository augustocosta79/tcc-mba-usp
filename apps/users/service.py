from typing import Optional
from uuid import UUID

from apps.shared.value_objects import Name, Email, Password
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.schema import UserUpdateSchema, UserActivationSchema
from apps.shared.exceptions import ConflictError, UnauthorizedError, NotFoundError
from apps.users.user_entity import User


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    def create_user(
        self, name: str, email: str, password: str, username: Optional[str] = None
    ) -> User:
        
        regsitered_user = self.repository.get_user_by_email(user_email=email)
        if regsitered_user is None:
            user = User(name=Name(name), email=Email(email), username=username, password=Password(password))
            saved_user = self.repository.save(user)
            return saved_user
                
        raise ConflictError("This e-mail is already in use")
        
        

    def get_user_by_id(self, user_id: UUID) -> User:
        if not (user := self.repository.get_user_by_id(user_id=user_id)):
            raise NotFoundError(f"User with id {user_id} not found")
        return user

    def list_users(self) -> list[User]:
        return self.repository.list_users()

    def update_user(self, user_id: UUID, payload: UserUpdateSchema) -> None:
        user = self.get_user_by_id(user_id=user_id)

        operations = {"name": user.rename, "username": user.change_username}

        for attr, value in payload.model_dump().items():
            if value is not None:
                operations[attr](value)

        updated_user = self.repository.update_user(user)
        if not updated_user:
            raise NotFoundError(f"Can't update user with id {user_id}. User not found")

        return updated_user


    def change_user_password(self, user_id: UUID, current_raw_password: str, new_raw_password: str) -> bool:
        user = self.get_user_by_id(user_id)
        
        if not user.password.verify(raw_password=current_raw_password):
            raise UnauthorizedError("Wrong password")
        
        user.change_password(current_raw_password, new_raw_password)
        self.repository.update_user(user)

    def user_activation(self, user_id: UUID, payload: UserActivationSchema) -> User:
        user = self.get_user_by_id(user_id=user_id)

        if payload.status is True:
            user.activate()
        else:
            user.deactivate()
            print("user deactivated")
        
        saved_user = self.repository.update_user(user=user)
        if not saved_user:
            raise NotFoundError(f"Can'activate user with id {user_id}. User not found.")

        return saved_user
    
    def delete_user(self, user_id:UUID) -> None:
        user = self.get_user_by_id(user_id=user_id)
        self.repository.delete_user(user_id=user.id)
        return