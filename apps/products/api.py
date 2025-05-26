import traceback
from http import HTTPStatus
from uuid import UUID

from apps.products.repository import ProductRepository
from apps.products.schema import ProductCreateSchema, ProductSchema
from apps.products.service import ProductService
from apps.shared.exceptions import NotFoundError
from apps.shared.value_objects import Description, Price, Stock, Title
from ninja import Router
from ninja.errors import HttpError
from utils.error_schema import ErrorSchema

products_router = Router()

repository = ProductRepository()
service = ProductService(repository)


@products_router.post(
    "",
    response={
        HTTPStatus.CREATED: ProductSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_product(request, payload: ProductCreateSchema):
    try:
        title = Title(payload.title)
        description = Description(payload.description)
        price = Price(payload.price)
        stock = Stock(payload.stock)
        owner_id = payload.owner_id

        created_product = service.create_product(
            title, description, price, stock, owner_id
        )

        return HTTPStatus.CREATED, ProductSchema(
            id=created_product.id,
            title=created_product.title.text,
            description=created_product.description.text,
            price=str(created_product.price.value),
            stock=created_product.stock.value,
            owner_id=created_product.owner_id,
            created_at=created_product.created_at,
            updated_at=created_product.updated_at,
        )
    except Exception as exc:
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


@products_router.get(
    "/{product_id}",
    response={HTTPStatus.OK: ProductSchema, HTTPStatus.NOT_FOUND: ErrorSchema},
)
def get_product_by_id(request, product_id: UUID):
    try:
        product = service.get_product_by_id(product_id)
        return ProductSchema(
            id=product.id,
            title=product.title.text,
            description=product.description.text,
            price=str(product.price.value),
            stock=product.stock.value,
            owner_id=product.owner_id,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
    except NotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
