from apps.users.models import UserModel
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email
from apps.users.repository import UserRepository
import pytest


@pytest.fixture
def create_user_and_repository():
        name=Name("Augusto")
        email=Email("amcneto@hotmail.com")
        username="amcneto"
        user = User(name=name, email=email, username=username)

        repository  = UserRepository()

        return user, repository

@pytest.mark.django_db
class TestUserRepository:
    def test_should_save_user(self, create_user_and_repository):
        user, repository = create_user_and_repository
        repository.save(user)

        persisted_user = UserModel.objects.get(id=user.id)

        assert persisted_user.id == user.id
        assert persisted_user.name == str(user.name)
        assert persisted_user.email == str(user.email)
        assert persisted_user.username == user.username
        assert persisted_user.is_active is True

    
    def test_should_get_user_by_id(self, create_user_and_repository):
        user, repository = create_user_and_repository

        repository.save(user=user)

        retrieved_used = repository.get_user_by_id(user_id=user.id)

        assert retrieved_used.id == user.id
        assert retrieved_used.name == str(user.name)
        assert retrieved_used.email == str(user.email)
        assert retrieved_used.username == user.username
        assert isinstance(retrieved_used, User)