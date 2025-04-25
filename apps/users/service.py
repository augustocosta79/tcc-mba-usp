from apps.users.user_entity import User

class UserService:
    def __init__(self, repository):
        self.repository = repository

    def create_user(self, name: str, email: str, username: str) -> User:
        user = User(name=name, email=email, username=username)
        self.repository.save(user)
        return user