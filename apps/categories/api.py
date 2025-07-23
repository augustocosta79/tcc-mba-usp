import traceback
from http import HTTPStatus
from uuid import UUID

from apps.categories.repository import CategoryRepository
from apps.categories.schema import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
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
    try:
        category = service.create_category(payload.name, payload.description or "")
        return HTTPStatus.CREATED, CategorySchema(
            id=category.id,
            name=category.name.value,
            description=category.description.text,
            created_at=category.created_at,
            updated_at=category.updated_at
        )
    except Exception as exc:
        logger.error(f"Unexpected error on POST /categories: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
    
@categories_router.get("", response={HTTPStatus.OK: list[CategorySchema]})
def list_categories(request):
    try:
        categories = service.list_categories()
        return [
            CategorySchema(
            id=category.id,
            name=category.name.value,
            description=category.description.text,
            created_at=category.created_at,
            updated_at=category.updated_at
            )
            for category in categories
        ]
    except Exception as exc:
        logger.error(f"Unexpected error on GET /categories: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
    
@categories_router.get("{category_id}", response={HTTPStatus.OK: CategorySchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def get_category_by_id(request, category_id:UUID):
    try:
        category = service.get_category_by_id(category_id)
        return CategorySchema(
            id=category.id,
            name=category.name.value,
            description=category.description.text,
            created_at=category.created_at,
            updated_at=category.updated_at
            )
    except Exception as exc:
        logger.error(f"Unexpected error on GET /categories/{category_id}: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
    
@categories_router.patch("{category_id}", response={HTTPStatus.OK: CategorySchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def update_category(request, category_id:UUID, payload: CategoryUpdateSchema):
    try:
        category = service.update_category(category_id, payload)
        return CategorySchema(
            id=category.id,
            name=category.name.value,
            description=category.description.text,
            created_at=category.created_at,
            updated_at=category.updated_at
            )
    except Exception as exc:
        logger.error(f"Unexpected error on PATCH /categories/{category_id}: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
    
@categories_router.delete("{category_id}", response={HTTPStatus.NO_CONTENT: None, HTTPStatus.NOT_FOUND: ErrorSchema})
def delete_category(request, category_id:UUID):
    if not (category:=service.get_category_by_id(category_id)):
        raise HttpError(HTTPStatus.NOT_FOUND, "Category not found")
    try:
        service.delete_category(category.id)
        return HTTPStatus.NO_CONTENT, None
    except Exception as exc:
        logger.error(f"Unexpected error on DELETE /categories/{category_id}: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))