from http import HTTPStatus
from typing import List
from uuid import UUID

from apps.products.repository import ProductRepository
from apps.products.schema import (
    ProductActivationSchema,
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema,
)
from apps.products.serializers import product_to_schema
from apps.products.service import ProductService
from ninja import Query, Router
from utils.error_schema import ErrorSchema
from utils.logger import configure_logger

products_router = Router()

repository = ProductRepository()
logger = configure_logger(__name__)
service = ProductService(repository, logger)


@products_router.post(
    "",
    response={
        HTTPStatus.CREATED: ProductSchema,
    },
)
def create_product(request, payload: ProductCreateSchema):
    created_product = service.create_product(
        payload.title,
        payload.description,
        payload.price,
        payload.stock,
        payload.owner_id,
        payload.categories,
    )
    return HTTPStatus.CREATED, product_to_schema(created_product)


@products_router.get(
    "/{product_id}",
    response={
        HTTPStatus.OK: ProductSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def get_product_by_id(request, product_id: UUID):
    product = service.get_product_by_id(product_id)
    return product_to_schema(product)


@products_router.get(
    "",
    response={
        HTTPStatus.OK: List[ProductSchema],
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def list_products_by_category(request, category_id: UUID = Query(...)):
    products = service.list_products_by_category(category_id)
    return [product_to_schema(product) for product in products]


@products_router.patch(
    "/{product_id}",
    response={
        HTTPStatus.OK: ProductSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_product(request, product_id: UUID, payload: ProductUpdateSchema):
    product = service.get_product_by_id(product_id)
    updated_product = service.update_product(product.id, payload)
    return product_to_schema(updated_product)


@products_router.patch(
    "{product_id}/activation",
    response={
        HTTPStatus.OK: ProductSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def product_activation(request, product_id: UUID, payload: ProductActivationSchema):
    product = service.product_activation(product_id, payload)
    return product_to_schema(product)


@products_router.delete(
    "/{product_id}",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def delete_product(request, product_id: UUID):
    service.delete_product(product_id)
    return HTTPStatus.NO_CONTENT, None
