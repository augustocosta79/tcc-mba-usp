from unittest.mock import MagicMock
from apps.users.service import UserService
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name
import pytest

class TestUserService:
    def test_should_create_user_with_valid_data(self):

        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        email="amcneto@hotmail.com",
        username="amcneto",
        name=Name("Augusto")
        
        user = service.create_user(
            name=name,
            email=email,
            username=username
        )

        assert isinstance(user, User)
        assert user.name == name
        assert user.email == email
        assert user.username == username
        assert user.is_active is True
        mock_repository.save.assert_called_once_with(user)