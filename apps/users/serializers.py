from apps.users.user_entity import User
from apps.users.schema import UserSchema

def user_to_schema(user: User) -> UserSchema:
    return UserSchema(
        id=user.id,
        name=user.name.value,
        email=user.email.value,
        username=user.username,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )