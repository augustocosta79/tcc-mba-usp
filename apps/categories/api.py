import traceback
from http import HTTPStatus
from uuid import UUID

from apps.categories.repository import CategoryRepository
from apps.categories.schema import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from apps.categories.serializers import category_to_schema
from apps.categories.service import CategoryService
from ninja import Router
from ninja.errors import HttpError
from utils.error_schema import ErrorSchema
from utils.logger import configure_logger

categories_router = Router()
repository = CategoryRepository()
logger = configure_logger(__name__)
service = CategoryService(repository, logger)


@categories_router.post("", response={HTTPStatus.CREATED: CategorySchema})
def create_category(request, payload: CategoryCreateSchema):
    category = service.create_category(payload.name, payload.description or "")
    return HTTPStatus.CREATED, category_to_schema(category)


@categories_router.get("", response={HTTPStatus.OK: list[CategorySchema]})
def list_categories(request):
    categories = service.list_categories()
    return [category_to_schema(category) for category in categories]


@categories_router.get(
    "{category_id}",
    response={HTTPStatus.OK: CategorySchema, HTTPStatus.NOT_FOUND: ErrorSchema},
)
def get_category_by_id(request, category_id: UUID):
    category = service.get_category_by_id(category_id)
    return category_to_schema(category)


@categories_router.patch(
    "{category_id}",
    response={HTTPStatus.OK: CategorySchema, HTTPStatus.NOT_FOUND: ErrorSchema},
)
def update_category(request, category_id: UUID, payload: CategoryUpdateSchema):
    category = service.update_category(category_id, payload)
    return category_to_schema(category)


@categories_router.delete(
    "{category_id}",
    response={HTTPStatus.NO_CONTENT: None, HTTPStatus.NOT_FOUND: ErrorSchema},
)
def delete_category(request, category_id: UUID):
    if not (category := service.get_category_by_id(category_id)):
        raise HttpError(HTTPStatus.NOT_FOUND, "Category not found")
    service.delete_category(category.id)
    return HTTPStatus.NO_CONTENT, None
