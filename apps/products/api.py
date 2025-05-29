import traceback
from http import HTTPStatus
from uuid import UUID

from apps.products.repository import ProductRepository
from apps.products.schema import ProductCreateSchema, ProductSchema, ProductUpdateSchema
from apps.products.service import ProductService
from apps.shared.exceptions import NotFoundError
from apps.shared.value_objects import Description, Price, Stock, Title
from ninja import Router
from ninja.errors import HttpError
from utils.error_schema import ErrorSchema
from typing import List

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
        category = payload.category

        created_product = service.create_product(
            title, description, price, stock, owner_id, category
        )

        return HTTPStatus.CREATED, ProductSchema(
            id=created_product.id,
            title=created_product.title.text,
            description=created_product.description.text,
            price=str(created_product.price.value),
            stock=created_product.stock.value,
            owner_id=created_product.owner_id,
            category=created_product.category,
            is_active=created_product.is_active,
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
            category=product.category,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )
    except NotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
    

@products_router.get(
    "",
    response={HTTPStatus.OK: List[ProductSchema]},
)
def list_products_by_category(request, category: str):
    products = service.list_products_by_category(category)
    return [
        ProductSchema(
            id=product.id,
            title=product.title.text,
            description=product.description.text,
            price=str(product.price.value),
            stock=product.stock.value,
            owner_id=product.owner_id,
            category=product.category,
            is_active=product.is_active,
            created_at=product.created_at,
            updated_at=product.updated_at,
        )

        for product in products
    ]

@products_router.patch("/{product_id}", response = {HTTPStatus.OK: ProductSchema, HTTPStatus.NOT_FOUND: ErrorSchema})
def update_product(request, product_id: UUID, payload: ProductUpdateSchema):
    try:
        product = service.get_product_by_id(product_id)
        updated_product = service.update_product(product.id, payload)

        return ProductSchema(
            id=updated_product.id,
            title=updated_product.title.text,
            description=updated_product.description.text,
            price=str(updated_product.price.value),
            stock=updated_product.stock.value,
            owner_id=updated_product.owner_id,
            category=updated_product.category,
            is_active=updated_product.is_active,
            created_at=updated_product.created_at,
            updated_at=updated_product.updated_at,
        )
    except NotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
    except Exception as exc:
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
