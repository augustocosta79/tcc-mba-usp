from typing import Optional
from uuid import UUID

from apps.shared.value_objects import Name, Email, Password
from apps.users.repository_interface import UserRepositoryInterface
from apps.users.schema import UserUpdateSchema, UserActivationSchema
from apps.shared.exceptions import ConflictError, UnauthorizedError, NotFoundError
from apps.users.user_entity import User

from utils.logger import configure_logger
import logging

logger = configure_logger(__name__)


class UserService:
    def __init__(self, repository: UserRepositoryInterface, logger: logging.Logger):
        self.repository = repository
        self.logger = logger

    def create_user(
        self, name: str, email: str, password: str, username: Optional[str] = None
    ) -> User:
        
        regsitered_user = self.repository.get_user_by_email(user_email=email)
        if regsitered_user is None:
            user = User(name=Name(name), email=Email(email), username=username, password=Password(password))
            saved_user = self.repository.save(user)
            self.logger.info(f"User for e-mail {saved_user.email.value} created successfully")
            return saved_user
                
        self.logger.warning(f"Conflict Error: {email} is already in use")
        raise ConflictError("This e-mail is already in use")
        
        

    def get_user_by_id(self, user_id: UUID) -> User:
        if not (user := self.repository.get_user_by_id(user_id=user_id)):
            raise NotFoundError(f"Can't get user with id {user_id}. User not found")
        return user

    def list_users(self) -> list[User]:
        return self.repository.list_users()

    def update_user(self, user_id: UUID, payload: UserUpdateSchema) -> User:
        user = self.repository.get_user_by_id(user_id=user_id)
        if not user:
            self.logger.warning(f"Can't update user with id {user_id}. User not found.")
            raise NotFoundError(f"Can't update user with id {user_id}. User not found")

        operations = {"name": user.rename, "username": user.change_username}

        for attr, value in payload.model_dump().items():
            if value is not None:
                operations[attr](value)

        updated_user = self.repository.update_user(user)
        self.logger.info(f"User {updated_user.email.value} updated successfully")
        return updated_user


    def change_user_password(self, user_id: UUID, current_raw_password: str, new_raw_password: str) -> bool:
        user = self.repository.get_user_by_id(user_id)

        if not user:
            self.logger.warning(f"Can't change user password for id {user_id}. User not found")
            raise NotFoundError(f"Can't change user password for id {user_id}. User not found")
        
        if not user.password.verify(raw_password=current_raw_password):
            self.logger.warning(f"Unauthorized attempt to change password for user id {user_id}: wrong current password.")
            raise UnauthorizedError(f"Unauthorized attempt to change password for user id {user_id}: wrong current password.")
        
        user.change_password(current_raw_password, new_raw_password)
        self.logger.info(f"Password updated successfully for user id {user_id}")
        self.repository.update_user(user)

    def user_activation(self, user_id: UUID, payload: UserActivationSchema) -> User:
        user = self.repository.get_user_by_id(user_id=user_id)
        if not user:
            self.logger.warning(f"Can't (de)activate user with id {user_id}. User not found.")
            raise NotFoundError(f"Can't (de)activate user with id {user_id}. User not found.")

        if payload.status is True:
            user.activate()
            self.logger.info(f"User with id {user.id} successfully activated")
        else:
            user.deactivate()
            self.logger.info(f"User with id {user.id} successfully deactivated")
        
        saved_user = self.repository.update_user(user=user)
        return saved_user
    
    def delete_user(self, user_id:UUID) -> None:
        user = self.repository.get_user_by_id(user_id=user_id)
        if not user:
            self.logger.warning(f"Can't delete user with id {user_id}. User not found.")
            raise NotFoundError(f"Can't delete user with id {user_id}. User not found.")
        self.repository.delete_user(user_id=user.id)
        self.logger.info(f"User {user.email.value} successfully deleted")
        return