from unittest.mock import MagicMock

import pytest
from apps.shared.exceptions import ConflictError, NotFoundError, UnauthorizedError
from apps.shared.value_objects import Email, Name, Password
from apps.users.schema import UserActivationSchema, UserUpdateSchema
from apps.users.service import UserService
from apps.users.user_entity import User


@pytest.fixture
def get_resources():
    repository_mock = MagicMock()
    logger_mock = MagicMock()
    service = UserService(repository=repository_mock, logger=logger_mock)

    return repository_mock, logger_mock, service

class TestServiceLogs:
    def test_should_log_user_creation_successfully(self):
        repository_mock = MagicMock()
        logger_mock = MagicMock()
        service = UserService(repository=repository_mock, logger=logger_mock)

        name = Name("Augusto")
        email = Email("amcneto@hotmail.com")
        username = "amcneto"
        raw_password = "Abc@1234"
        password = Password(raw_password)

        user = User(name=name, email=email, username=username, password=password)
        repository_mock.save.return_value = user
        repository_mock.get_user_by_email.return_value = None

        service.create_user(
            name=name.value, email=email.value, username=username, password=raw_password
        )

        logger_mock.info.assert_called_once()
        assert (
            f"User for e-mail {email.value} created successfully"
            in logger_mock.info.call_args[0][0]
        )


    def test_should_log_conflict_error_successfully(self):
        repository_mock = MagicMock()
        logger_mock = MagicMock()
        service = UserService(repository=repository_mock, logger=logger_mock)

        name = Name("Augusto")
        email = Email("amcneto@hotmail.com")
        username = "amcneto"
        raw_password = "Abc@1234"
        password = Password(raw_password)

        user = User(name=name, email=email, username=username, password=password)
        repository_mock.save.return_value = user
        repository_mock.get_user_by_email.return_value = user

        with pytest.raises(ConflictError):
            service.create_user(
                name=name.value, email=email.value, username=username, password=raw_password
            )

        logger_mock.warning.assert_called_once()
        assert (
            f"Conflict Error: {email.value} is already in use"
            in logger_mock.warning.call_args[0][0]
        )


    def test_should_log_user_update_successfully(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = user_mock
        repository_mock.update_user.return_value = user_mock
        payload = UserUpdateSchema(name="New Name")
        service.update_user(user_id=user_mock.id, payload=payload)

        logger_mock.info.assert_called_once()
        assert "updated successfully" in logger_mock.info.call_args[0][0]


    def test_should_log_not_found_successfully_to_update_absent_user(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = None
        payload = UserUpdateSchema(name="New Name")

        with pytest.raises(NotFoundError):
            service.update_user(user_id=user_mock.id, payload=payload)

        logger_mock.warning.assert_called_once()
        assert "User not found" in logger_mock.warning.call_args[0][0]


    def test_should_log_password_change_successfully(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        current_pass = "any pass"
        new_pass = "any new pass"
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = user_mock
        user_mock.password.verify.return_value = True
        service.change_user_password(user_mock.id, current_pass, new_pass)

        logger_mock.info.assert_called_once()
        assert "Password updated successfully" in logger_mock.info.call_args[0][0]


    def test_should_log_password_change_failure_wrong_password(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        current_pass = "any pass"
        new_pass = "any new pass"
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = user_mock
        user_mock.password.verify.return_value = False

        with pytest.raises(UnauthorizedError):
            service.change_user_password(user_mock.id, current_pass, new_pass)
        logger_mock.warning.assert_called_once()
        assert "wrong current password" in logger_mock.warning.call_args[0][0]


    def test_should_log_password_change_failure_wrong_user_id(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        current_pass = "any pass"
        new_pass = "any new pass"
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = None

        with pytest.raises(NotFoundError):
            service.change_user_password(user_mock.id, current_pass, new_pass)
        logger_mock.warning.assert_called_once()
        assert "User not found" in logger_mock.warning.call_args[0][0]


    def test_should_log_user_activation_successfully(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        payload = UserActivationSchema(status=True)
        repository_mock.get_user_by_id.return_value = user_mock
        service.user_activation(user_mock.id, payload)

        logger_mock.info.assert_called_once()
        assert "successfully activated" in logger_mock.info.call_args[0][0]


    def test_should_log_user_activation_failure(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        payload = UserActivationSchema(status=True)
        repository_mock.get_user_by_id.return_value = None

        with pytest.raises(NotFoundError):
            service.user_activation(user_mock.id, payload)
        logger_mock.warning.assert_called_once()
        assert "Can't (de)activate user" in logger_mock.warning.call_args[0][0]


    def test_should_log_user_deactivation_successfully(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        payload = UserActivationSchema(status=False)
        repository_mock.get_user_by_id.return_value = user_mock
        service.user_activation(user_mock.id, payload)

        logger_mock.info.assert_called_once()
        assert "successfully deactivated" in logger_mock.info.call_args[0][0]


    def test_should_log_user_deletion_successfully(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = user_mock
        service.delete_user(user_mock.id)

        logger_mock.info.assert_called_once()
        assert (
            f"User {user_mock.email.value} successfully deleted"
            in logger_mock.info.call_args[0][0]
        )


    def test_should_log_user_deletion_failure(self, get_resources):
        repository_mock, logger_mock, service = get_resources
        user_mock = MagicMock()
        repository_mock.get_user_by_id.return_value = None

        with pytest.raises(NotFoundError):
            service.delete_user(user_mock.id)
        logger_mock.warning.assert_called_once()
        assert "User not found" in logger_mock.warning.call_args[0][0]
