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