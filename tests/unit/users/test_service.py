from unittest.mock import MagicMock
from apps.users.service import UserService
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email
from uuid import UUID
import pytest

class TestUserService:
    def test_should_create_user_with_valid_data(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        email=Email("amcneto@hotmail.com")
        username="amcneto"
        name=Name("Augusto")
        
        user = service.create_user(
            name=name,
            email=email,
            username=username
        )

        assert isinstance(user, User)
        assert isinstance(user.id, UUID)
        assert user.name == name
        assert user.email == email
        assert user.username == username
        assert user.is_active is True
        mock_repository.save.assert_called_once_with(user)

    
    def test_should_get_user_by_id(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        name = Name("Test")
        email = Email("test@email.com")
        username = "username123"

        user = User(name, email, username)

        mock_repository.get_user_by_id.return_value = user

        retrieved_user = service.get_user_by_id(user_id=user.id)

        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email
        assert retrieved_user.username == user.username
        assert isinstance(retrieved_user, User)
        mock_repository.get_user_by_id.assert_called_once_with(user_id=user.id)

    
    def test_should_get_users_list(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        name1 = Name("TestOne")
        email1 = Email("test1@email.com")
        username1 = "username123"

        user1 = User(name1, email1, username1)

        name2 = Name("TestTwo")
        email2 = Email("test2@email.com")
        username2 = "username234"

        user2 = User(name2, email2, username2)


        mock_repository.list_users.return_value = [user1, user2]

        users = service.list_users()

        assert isinstance(users, list)
        assert user1 in users
        assert user2 in users
        assert len(users) == 2
        mock_repository.list_users.assert_called_once()