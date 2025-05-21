import pytest

import json

from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.users.schema import UserUpdateSchema, UserActivationSchema, UserPasswordSchema
from apps.shared.value_objects import Email, Name, Password

repository = UserRepository()
service = UserService(repository=repository)

name = Name("Test")
email = Email("test@email.com")
raw_password = "Abc@1234"
password = Password(raw_password)
username = "testeusername"

@pytest.fixture
def create_test_user():
    user = service.create_user(name=name, email=email, password=password, username=username)

    return user


@pytest.mark.django_db
class TestCreateUser:
    def test_should_create_user_successfully(self, client):
        payload = {
            "name": "Augusto",
            "email": "test@email.com",
            "username": "augustocosta",
            "password": "Abc@1234"
        }

        response = client.post(
            "/api/users",
            data=json.dumps(payload),
            content_type="application/json"
        )

        assert response.status_code == 201
        body = response.json()

        assert "id" in body
        assert body["name"] == payload["name"]
        assert body["email"] == payload["email"]
        assert body["username"] == payload["username"]
        assert "password" not in body

@pytest.mark.django_db
class TestListUsers:
    def test_should_list_users_successfully(self, client, create_test_user):
        user = create_test_user
        response = client.get("/api/users")

        assert response.status_code == 200
        body = response.json()

        created_user_data = body[0]

        assert created_user_data["id"] == str(user.id)
        assert created_user_data["name"] == user.name.value
        assert created_user_data["email"] == user.email.value
        assert "password" not in created_user_data

@pytest.mark.django_db
class TestGetUserById:
    def test_should_get_user_by_id_successfully(self, client, create_test_user):
        user = create_test_user

        response = client.get(f"/api/users/{user.id}")
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] == user.is_active

@pytest.mark.django_db
class TestUpdateUser:
    def test_should_update_user_name(self, client, create_test_user):
        user = create_test_user

        new_name = "New Test Name"
        payload = UserUpdateSchema(name=new_name)

        response = client.patch(
            f"/api/users/{user.id}",
            payload.model_dump(),
            content_type="application/json"
        )
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == str(user.id)
        assert body["name"] == new_name
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] == user.is_active

    def test_should_update_user_username(self, client, create_test_user):
        user = create_test_user

        new_username = "New Test Username"
        payload = UserUpdateSchema(username=new_username)

        response = client.patch(
            f"/api/users/{user.id}",
            payload.model_dump(),
            content_type="application/json"
        )
        assert response.status_code == 200

        body = response.json()
        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == new_username
        assert body["is_active"] == user.is_active

@pytest.mark.django_db
class TestUserActivation:
    def test_should_deactivate_user_successfully(self, client, create_test_user):
        user = create_test_user

        payload = UserActivationSchema(status=False)

        response = client.patch(
            f"/api/users/{user.id}/activation",
            payload.model_dump(),
            content_type="application/json"
        )
        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] is False

    def test_should_activate_user_successfully(self, client, create_test_user):
        user = create_test_user
        user.deactivate()
        repository.update_user(user=user)

        payload = UserActivationSchema(status=True)

        response = client.patch(
            f"/api/users/{user.id}/activation",
            payload.model_dump(),
            content_type="application/json"
        )
        assert response.status_code == 200

        body = response.json()

        assert body["id"] == str(user.id)
        assert body["name"] == user.name.value
        assert body["email"] == user.email.value
        assert body["username"] == user.username
        assert body["is_active"] is True

@pytest.mark.django_db
class TestChangeUserPassword:
    def test_should_change_user_password_successfully(self, client, create_test_user):
        user = create_test_user

        new_raw_password = "abC@1234"

        payload = UserPasswordSchema(current_password=raw_password, new_password=new_raw_password)

        response = client.patch(
            f"/api/users/{user.id}/password",
            payload.model_dump(),
            content_type="application/json"
        )
        assert response.status_code == 204

        updated_user = repository.get_user_by_id(user_id=user.id)

        assert updated_user.password.verify(new_raw_password)

@pytest.mark.django_db
class TestDeleteUser:
    def test_should_delete_user_successfully(self, client, create_test_user):
        user = create_test_user

        response = client.delete(f"/api/users/{user.id}")

        assert response.status_code == 204
