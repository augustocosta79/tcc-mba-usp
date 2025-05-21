from apps.users.models import UserModel
from apps.users.user_entity import User
from apps.shared.value_objects.name import Name
from apps.shared.value_objects.email import Email
from apps.shared.value_objects.password import Password
from apps.users.repository import UserRepository
from apps.shared.exceptions import ConflictError
import pytest


@pytest.fixture
def create_user_and_repository():
        name=Name("Augusto")
        email=Email("amcneto@hotmail.com")
        username="amcneto"
        raw_password = "Abc@1234"
        password = Password(raw_password)
        user = User(name=name, email=email, username=username, password=password)

        repository  = UserRepository()
        saved_user = repository.save(user)

        return saved_user, repository, raw_password

@pytest.mark.django_db
class TestUserRepository:
    def test_should_save_user_successfully(self, create_user_and_repository):
        user, repository, raw_password = create_user_and_repository

        persisted_user = repository.get_user_by_id(user_id=user.id)

        assert persisted_user.id == user.id
        assert persisted_user.name.value == user.name.value
        assert persisted_user.email.value == user.email.value
        assert persisted_user.username == user.username
        assert persisted_user.password.verify(raw_password) is True
        assert persisted_user.is_active is True

    
    def test_should_get_user_by_id(self, create_user_and_repository):
        user, repository, raw_password = create_user_and_repository
        
        retrieved_used = repository.get_user_by_id(user_id=user.id)

        assert retrieved_used.id == user.id
        assert retrieved_used.name.value == str(user.name)
        assert retrieved_used.email.value == str(user.email)
        assert retrieved_used.username == user.username
        assert retrieved_used.password.verify(raw_password)
        assert isinstance(retrieved_used, User)

    def test_should_delete_user(self, create_user_and_repository):
         user, repository, raw_password = create_user_and_repository
         
         repository.delete_user(user.id)
         
         assert repository.get_user_by_id(user.id) is None

    def test_should_get_user_by_email(self, create_user_and_repository):
        user, repository, raw_password = create_user_and_repository
        retrieved_user = repository.get_user_by_email(user_email=user.email.value)

        assert retrieved_user.id == user.id
        assert retrieved_user.name.value == str(user.name)
        assert retrieved_user.email.value == str(user.email)
        assert retrieved_user.username == user.username
        assert retrieved_user.password.verify(raw_password)
        assert isinstance(retrieved_user, User)
         