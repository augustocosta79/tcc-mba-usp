from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
from apps.shared.value_objects.email import Email
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.password import Password
from apps.users.service import UserService
from apps.users.user_entity import User
from apps.users.schema import UserUpdateSchema, UserActivationSchema
from apps.users.models import UserModel
from apps.shared.exceptions import UnauthorizedError, ConflictError, NotFoundError


class TestUserService:
    def test_should_create_user_with_valid_data(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        email=Email("amcneto@hotmail.com")
        username="amcneto"
        name=Name("Augusto")
        raw_password = "Abc@1234"
        password=Password(raw_password)

        mock_repository.get_user_by_email.return_value = None
        
        user = service.create_user(
            name=name,
            email=email,
            username=username,
            password=password
        )

        assert isinstance(user, User)
        assert isinstance(user.id, UUID)
        assert user.name == name
        assert user.email == email
        assert user.username == username
        assert user.is_active is True
        assert isinstance(user.password, Password)
        assert user.password is not None
        assert user.password.verify(raw_password)
        mock_repository.save.assert_called_once_with(user)

    def test_should_raise_conflict_error_for_duplicated_email(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        name=Name("Augusto")
        email=Email("amcneto@hotmail.com")
        username="amcneto"
        raw_password = "Abc@1234"
        password=Password(raw_password)

        mock_repository.get_user_by_email.return_value = email.value
        
        with pytest.raises(ConflictError):
            user = service.create_user(
                name=name,
                email=email,
                username=username,
                password=password
            )

    
    def test_should_get_user_by_id(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        name = Name("Test")
        email = Email("test@email.com")
        username = "username123"
        raw_password = "Abc@1234"
        password=Password(raw_password)

        user = User(name=name, email=email, username=username, password=password)

        mock_repository.get_user_by_id.return_value = user

        retrieved_user = service.get_user_by_id(user_id=user.id)

        assert retrieved_user.id == user.id
        assert retrieved_user.name == user.name
        assert retrieved_user.email == user.email
        assert retrieved_user.username == user.username
        assert retrieved_user.password is not None
        assert retrieved_user.password.verify(raw_password)
        assert isinstance(retrieved_user, User)
        mock_repository.get_user_by_id.assert_called_once_with(user_id=user.id)

    def test_should_raise_not_found_error_for_wrong_user_id(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)
        random_id = uuid4()
        mock_repository.get_user_by_id.return_value = None

        with pytest.raises(NotFoundError):
            service.get_user_by_id(user_id=random_id)

    
    def test_should_get_users_list(self):
        mock_repository = MagicMock()
        service = UserService(repository=mock_repository)

        name1 = Name("TestOne")
        email1 = Email("test1@email.com")
        username1 = "username123"
        raw_password = "Abc@1234"
        password=Password(raw_password)

        user1 = User(name=name1, email=email1, username=username1, password=password)

        name2 = Name("TestTwo")
        email2 = Email("test2@email.com")
        username2 = "username234"

        user2 = User(name=name2, email=email2, username=username2, password=password)


        mock_repository.list_users.return_value = [user1, user2]

        users = service.list_users()

        assert isinstance(users, list)
        assert user1 in users
        assert user2 in users
        assert len(users) == 2
        mock_repository.list_users.assert_called_once()

    def test_should_update_user(self):
        mock_user = MagicMock()
        mock_repository = MagicMock()
        fake_id = "any-fake-id"
        payload = UserUpdateSchema(name="New Name")
        service = UserService(repository=mock_repository)

        mock_repository.get_user_by_id.return_value = mock_user

        service.update_user(user_id=fake_id, payload=payload)

        mock_repository.get_user_by_id.assert_called_once_with(user_id=fake_id)
        mock_user.rename.assert_called_once_with(payload.name)
        mock_repository.update_user.assert_called_once_with(mock_user)

    def test_should_raise_not_found_error_to_update_not_found_user(self):
        mock_user = MagicMock()
        mock_repository = MagicMock()
        fake_id = "any-fake-id"
        payload = UserUpdateSchema(name="New Name")
        service = UserService(repository=mock_repository)

        mock_repository.get_user_by_id.return_value = mock_user
        mock_repository.update_user.return_value = None

        with pytest.raises(NotFoundError):
            service.update_user(user_id=fake_id, payload=payload)

    def test_should_change_user_password(self):
        mock_repository = MagicMock()
        mock_user = MagicMock()

        current_raw_password = "Abc@1234"
        new_raw_password = "Abc@2345"

        fake_id = "id-for-test"

        service = UserService(repository=mock_repository)

        mock_repository.get_user_by_id.return_value = mock_user

        service.change_user_password(user_id=fake_id, current_raw_password=current_raw_password, new_raw_password=new_raw_password)

        mock_repository.get_user_by_id.assert_called_once_with(user_id=fake_id)
        mock_user.change_password.assert_called_once_with(current_raw_password, new_raw_password)
        mock_repository.update_user.assert_called_once_with(mock_user)

    def test_should_raise_error_on_change_user_with_wrong_password(self):
        mock_repository = MagicMock()
        
        mock_user = MagicMock()
        mock_user.password.verify.return_value = False

        current_raw_password = "Abc@1234"
        new_raw_password = "Abc@2345"

        fake_id = "id-for-test"

        service = UserService(repository=mock_repository)
        service.get_user_by_id = MagicMock(return_value=mock_user)

        with pytest.raises(UnauthorizedError):
            service.change_user_password(user_id=fake_id, current_raw_password=current_raw_password, new_raw_password=new_raw_password)

        

    def test_should_deactivate_user_successfully(self):
        mock_user = MagicMock()
        mock_repository = MagicMock()
        fake_id = "any-fake-id"
        payload = UserActivationSchema(status=False)
        service = UserService(repository=mock_repository)

        mock_repository.get_user_by_id.return_value = mock_user

        service.user_activation(user_id=fake_id, payload=payload)


        mock_repository.get_user_by_id.assert_called_once_with(user_id=fake_id)
        mock_user.deactivate.assert_called_once()
        mock_repository.update_user.assert_called_once_with(user=mock_user)

    def test_should_activate_user_successfully(self):
        mock_user = MagicMock()
        mock_repository = MagicMock()
        fake_id = "any-fake-id"
        payload = UserActivationSchema(status=True)
        service = UserService(repository=mock_repository)

        mock_repository.get_user_by_id.return_value = mock_user

        service.user_activation(user_id=fake_id, payload=payload)


        mock_repository.get_user_by_id.assert_called_once_with(user_id=fake_id)
        mock_user.activate.assert_called_once()
        mock_repository.update_user.assert_called_once_with(user=mock_user)

    def test_should_raise_not_found_error_to_activate_not_found_user(self):
        mock_user = MagicMock()
        mock_repository = MagicMock()
        fake_id = "any-fake-id"
        payload = UserActivationSchema(status=True)
        service = UserService(repository=mock_repository)

        mock_repository.update_user.return_value = None
        service.get_user_by_id = MagicMock(return_value=mock_user)

        with pytest.raises(NotFoundError):
            service.user_activation(user_id=fake_id, payload=payload)

    def test_should_delete_user(self):
        mock_repository = MagicMock()
        mock_user = MagicMock()
        fake_id = "any-fake-id"

        service = UserService(repository=mock_repository)

        mock_repository.get_user_by_id.return_value = mock_user
        service.delete_user(user_id=fake_id)

        mock_repository.get_user_by_id.assert_called_once_with(user_id=fake_id)
        mock_repository.delete_user.assert_called_once_with(user_id=mock_user.id)

    def test_should_fail_when_email_already_in_use(self):
        mock_repository = MagicMock()
        mock_user = MagicMock()
        mock_repository.get_user_by_email.return_value = mock_user

        
        service = UserService(repository=mock_repository)

        email=Email("amcneto@hotmail.com")
        username="amcneto"
        name=Name("Augusto")
        raw_password = "Abc@1234"
        password=Password(raw_password)
        

        with pytest.raises(ConflictError):
            service.create_user(
            name=name,
            email=email,
            username=username,
            password=password
        )