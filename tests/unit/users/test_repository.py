from datetime import datetime

import pytest
from apps.shared.value_objects import Email, Name, Password
from apps.users.repository import UserRepository
from apps.users.entity import User


@pytest.fixture
def create_user_and_repository():
    name = Name("Augusto")
    email = Email("amcneto@hotmail.com")
    username = "amcneto"
    raw_password = "Abc@1234"
    password = Password(raw_password)
    user = User(name=name, email=email, username=username, password=password)

    repository = UserRepository()
    saved_user = repository.save(user)

    return user, repository, raw_password, saved_user


@pytest.mark.django_db
class TestUserRepository:
    def test_should_save_user_successfully(self, create_user_and_repository):
        user, repository, raw_password, saved_user = create_user_and_repository

        assert saved_user.id == user.id
        assert saved_user.name.value == user.name.value
        assert saved_user.email.value == user.email.value
        assert saved_user.username == user.username
        assert saved_user.password.verify(raw_password) is True
        assert saved_user.is_active is True
        assert saved_user.created_at is not None
        assert isinstance(saved_user.created_at, datetime)
        assert saved_user.updated_at is not None
        assert isinstance(saved_user.updated_at, datetime)

    def test_should_get_user_by_id(self, create_user_and_repository):
        user, repository, raw_password, saved_user = create_user_and_repository

        retrieved_user = repository.get_user_by_id(user_id=user.id)

        assert retrieved_user.id == user.id
        assert retrieved_user.name.value == str(user.name)
        assert retrieved_user.email.value == str(user.email)
        assert retrieved_user.username == user.username
        assert retrieved_user.password.verify(raw_password)
        assert isinstance(retrieved_user, User)
        assert retrieved_user.created_at == saved_user.created_at
        assert retrieved_user.updated_at == saved_user.updated_at

    def test_should_delete_user(self, create_user_and_repository):
        user, repository, raw_password, saved_user = create_user_and_repository

        repository.delete_user(user.id)

        assert repository.get_user_by_id(user.id) is None

    def test_should_get_user_by_email(self, create_user_and_repository):
        user, repository, raw_password, saved_user = create_user_and_repository
        retrieved_user = repository.get_user_by_email(user_email=user.email.value)

        assert retrieved_user.id == user.id
        assert retrieved_user.name.value == str(user.name)
        assert retrieved_user.email.value == str(user.email)
        assert retrieved_user.username == user.username
        assert retrieved_user.password.verify(raw_password)
        assert isinstance(retrieved_user, User)

    def test_should_update_user_successfully(self, create_user_and_repository):
        user, repository, raw_password, saved_user = create_user_and_repository

        new_name = "changed name"

        new_username = "new username"

        new_password = "New@1234"

        saved_user.rename(new_name)
        saved_user.change_username(new_username)
        current_password_hash = saved_user.password.hash
        saved_user.change_password(raw_password, new_password)
        saved_user.deactivate()

        updated_user = repository.update_user(saved_user)

        assert updated_user.name.value == new_name
        assert updated_user.username == new_username
        assert updated_user.password.hash != current_password_hash
        assert updated_user.is_active is False
        assert updated_user.updated_at > saved_user.updated_at

        saved_user.activate()
        last_updated_at = updated_user.updated_at
        updated_user = repository.update_user(saved_user)
        assert updated_user.is_active is True
        assert updated_user.updated_at > last_updated_at
