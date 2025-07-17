from uuid import UUID
from ninja import Router
from ninja.errors import HttpError
from http import HTTPStatus
from apps.categories.schema import CategorySchema, CategoryCreateSchema
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
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
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
    
@categories_router.get("{category_id}", response={HTTPStatus.OK: CategorySchema})
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
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))