import json
from uuid import uuid4

import pytest
from apps.users.repository import UserRepository
from apps.users.schema import UserActivationSchema, UserPasswordSchema, UserUpdateSchema
from apps.users.service import UserService
from tests.utils import assert_has_valid_timestamps
from tests.utils.timed_client import TimedClient
from utils.logger import configure_logger

repository = UserRepository()
logger = configure_logger(__name__)
service = UserService(repository=repository, logger=logger)

name = "Test"
email = "test@email.com"
password = "Abc@1234"
username = "testeusername"


@pytest.fixture
def timed_client(client):
    return TimedClient(client)

@pytest.fixture
def create_test_user():
    user = service.create_user(
        name=name, email=email, password=password, username=username
    )

    return user


@pytest.mark.django_db
class TestCreateUser:
    def test_should_return_status_201_created_and_user_data(self, timed_client):
        payload = {
            "name": "Augusto",
            "email": "test@email.com",
            "username": "augustocosta",
            "password": "Abc@1234",
        }

        response = timed_client.post(
            "/api/users", data=json.dumps(payload), content_type="application/json"
        )

        assert response.status_code == 201
        body = response.json()

        assert "id" in body
        assert body["name"] == payload["name"]
        assert body["email"] == payload["email"]
        assert body["username"] == payload["username"]
        assert "password" not in body
        assert "created_at" in body
        assert_has_valid_timestamps(body)



@pytest.mark.django_db
class TestListUsers:
    def test_should_return_status_200_ok_and_list_users_data(self, timed_client, create_test_user):
        user = create_test_user
        response = timed_client.get("/api/users")

        assert response.status_code == 200
        body = response.json()

        created_user_data = body[0]

        assert created_user_data["id"] == str(user.id)
        assert created_user_data["name"] == user.name.value
        assert created_user_data["email"] == user.email.value
        assert "password" not in created_user_data
        assert_has_valid_timestamps(created_user_data)


@pytest.mark.django_db
class TestGetUserById:
    def test_should_return_status_200_ok_and_user_data(self, timed_client, create_test_user):
        user = create_test_user

        response = timed_client.get(f"/api/users/{user.id}")
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] == user.is_active
        assert_has_valid_timestamps(body)


    def test_should_return_status_404_not_found_for_invalid_user_id(self, timed_client):
        response = timed_client.get(f"/api/users/{uuid4()}")
        assert response.status_code == 404
        "User not found" in response.json()["message"]

@pytest.mark.django_db
class TestUpdateUser:
    def test_should_return_status_200_ok_and_user_data_with_updated_name(self, timed_client, create_test_user):
        user = create_test_user

        new_name = "New Test Name"
        payload = UserUpdateSchema(name=new_name)

        response = timed_client.patch(
            f"/api/users/{user.id}",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == str(user.id)
        assert body["name"] == new_name
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] == user.is_active
        assert_has_valid_timestamps(body)

    def test_should_return_status_200_ok_and_user_data_with_updated_username(self, timed_client, create_test_user):
        user = create_test_user

        new_username = "New Test Username"
        payload = UserUpdateSchema(username=new_username)

        response = timed_client.patch(
            f"/api/users/{user.id}",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == new_username
        assert body["is_active"] == user.is_active
        assert_has_valid_timestamps(body)
    
    def test_should_return_status_404_not_found_for_invalid_user_id(self, timed_client, create_test_user):
        response = timed_client.patch(
            f"/api/users/{uuid4()}",
            {"name": "test name"},
            content_type="application/json",
        )
        assert response.status_code == 404
        assert "User not found" in response.json()["message"]


@pytest.mark.django_db
class TestUserActivation:
    def test_should_return_status_200_ok_and_deactivate_user(self, timed_client, create_test_user):
        user = create_test_user

        payload = UserActivationSchema(status=False)

        response = timed_client.patch(
            f"/api/users/{user.id}/activation",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] is False
        assert_has_valid_timestamps(body)

    def test_should_return_status_200_ok_and_activate_user(self, timed_client, create_test_user):
        user = create_test_user
        user.deactivate()
        repository.update_user(user=user)

        payload = UserActivationSchema(status=True)

        response = timed_client.patch(
            f"/api/users/{user.id}/activation",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] is True
        assert_has_valid_timestamps(body)
    
    
    def test_should_return_status_404_not_found_for_invalid_user_id(self, timed_client, create_test_user):
        response = timed_client.patch(
            f"/api/users/{uuid4()}/activation",
            {"status": True},
            content_type="application/json",
        )
        assert response.status_code == 404
        assert "User not found" in response.json()["message"]


@pytest.mark.django_db
class TestChangeUserPassword:
    def test_should_return_status_204_no_content_and_change_user_password_successfully(self, timed_client, create_test_user):
        user = create_test_user

        new_password = "abC@1234"

        payload = UserPasswordSchema(
            current_password=password, new_password=new_password
        )

        response = timed_client.patch(
            f"/api/users/{user.id}/password",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 204

        updated_user = repository.get_user_by_id(user_id=user.id)

        assert updated_user.password.verify(new_password)


    def test_should_return_status_401_unauthorized_for_wrong_current_password(self, timed_client, create_test_user):
        user = create_test_user

        new_password = "abC@1234"

        payload = UserPasswordSchema(
            current_password="aBc@1234", new_password=new_password
        )

        response = timed_client.patch(
            f"/api/users/{user.id}/password",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 401
        assert "wrong current password" in response.json()["message"]
    
    def test_should_return_status_404_not_found_for_invalid_user_id(self, timed_client):
        new_password = "abC@1234"

        payload = UserPasswordSchema(
            current_password=password, new_password=new_password
        )

        response = timed_client.patch(
            f"/api/users/{uuid4()}/password",
            payload.model_dump(),
            content_type="application/json",
        )
        assert response.status_code == 404
        assert "User not found" in response.json()["message"]


@pytest.mark.django_db
class TestDeleteUser:
    def test_should_return_201_no_content_adn_delete_user_successfully(self, timed_client, create_test_user):
        user = create_test_user
        response = timed_client.delete(f"/api/users/{user.id}")
        assert response.status_code == 204

    def test_should_return_404_not_found_for_invalid_user_id(self, timed_client, create_test_user):
        user = create_test_user
        response = timed_client.delete(f"/api/users/{user.id}")
        assert response.status_code == 204
