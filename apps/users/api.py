import traceback
from http import HTTPStatus
from uuid import UUID

from apps.shared.decorators.require_active_user import require_active_user
from apps.shared.exceptions import ConflictError
from apps.users.repository import UserRepository
from apps.users.schema import (
    UserActivationSchema,
    UserCreateSchema,
    UserPasswordSchema,
    UserSchema,
    UserUpdateSchema,
)
from apps.users.serializers import user_to_schema
from apps.users.service import UserService
from ninja import Router
from ninja.errors import HttpError
from utils.error_schema import ErrorSchema
from utils.logger import configure_logger

users_router = Router()
repository = UserRepository()
logger = configure_logger(__name__)
service = UserService(repository=repository, logger=logger)


@users_router.post(
    "",
    response={
        HTTPStatus.CREATED: UserSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
        HTTPStatus.CONFLICT: ErrorSchema,
    },
)
def create_user(request, payload: UserCreateSchema):
    try:
        user = service.create_user(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            username=payload.username,
        )
        return HTTPStatus.CREATED, user_to_schema(user)
    except ConflictError as e:
        raise HttpError(HTTPStatus.CONFLICT, str(e))
    except Exception as e:
        logger.error(f"Unexpected error on POST /users: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@users_router.get("", response={HTTPStatus.OK: list[UserSchema]})
def list_users(request):
    try:
        users = service.list_users()
        return [user_to_schema(user) for user in users]
    except Exception as e:
        logger.error(f"Unexpected error on GET /users: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@users_router.get("/{user_id}", response={HTTPStatus.OK: UserSchema})
def get_user_by_id(request, user_id: UUID):
    try:
        user = service.get_user_by_id(user_id=user_id)
        return user_to_schema(user)
    except Exception as e:
        logger.error(f"Unexpected error on GET /users/{user_id}: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@users_router.patch("/{user_id}", response={HTTPStatus.OK: UserSchema})
# @require_active_user
def update_user(request, user_id: UUID, payload: UserUpdateSchema):
    try:
        user = service.update_user(user_id=user_id, payload=payload)
        return user_to_schema(user)
    except Exception as e:
        logger.error(f"Unexpected error on PATCH /users/{user_id}: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@users_router.patch("/{user_id}/activation", response={HTTPStatus.OK: UserSchema})
def user_activation(request, user_id: UUID, payload: UserActivationSchema):
    try:
        user = service.get_user_by_id(user_id=user_id)
        deactivated_user = service.user_activation(user_id=user.id, payload=payload)
        return user_to_schema(deactivated_user)
    except Exception as e:
        logger.error(f"Unexpected error on PATCH /users/{user_id}/activation: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@users_router.patch("/{user_id}/password", response={HTTPStatus.NO_CONTENT: None})
# @require_active_user
def change_user_password(request, user_id: UUID, payload: UserPasswordSchema):
    try:
        service.change_user_password(
            user_id, payload.current_password, payload.new_password
        )
        return
    except Exception as e:
        logger.error(f"Unexpected error on PATCH /users/{user_id}/password: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))


@users_router.delete("/{user_id}", response={HTTPStatus.NO_CONTENT: None})
def delete_user(request, user_id: UUID):
    try:
        service.delete_user(user_id=user_id)
        return
    except Exception as e:
        logger.error(f"Unexpected error on DELETE /users/{user_id}: {str(e)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
