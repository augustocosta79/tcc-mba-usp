import traceback
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
from apps.shared.exceptions import NotFoundError
from ninja import Query, Router
from ninja.errors import HttpError
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
    try:
        created_product = service.create_product(
            payload.title,
            payload.description,
            payload.price,
            payload.stock,
            payload.owner_id,
            payload.categories,
        )

        return HTTPStatus.CREATED, product_to_schema(created_product)
    except Exception as exc:
        logger.error(f"Unexpected error on POST /products: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


@products_router.get(
    "/{product_id}",
    response={HTTPStatus.OK: ProductSchema, HTTPStatus.NOT_FOUND: ErrorSchema},
)
def get_product_by_id(request, product_id: UUID):
    try:
        product = service.get_product_by_id(product_id)
        return product_to_schema(product)
    except NotFoundError as exc:
        traceback.print_exc()
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
    except Exception as exc:
        logger.error(f"Unexpected error on POST /products: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


@products_router.get(
    "",
    response={HTTPStatus.OK: List[ProductSchema]},
)
def list_products_by_category(request, category_id: UUID = Query(...)):
    try:
        products = service.list_products_by_category(category_id)
        return [product_to_schema(product) for product in products]
    except Exception as exc:
        logger.error(f"Unexpected error on GET /products/{category_id}: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


@products_router.patch(
    "/{product_id}",
    response={HTTPStatus.OK: ProductSchema, HTTPStatus.NOT_FOUND: ErrorSchema},
)
def update_product(request, product_id: UUID, payload: ProductUpdateSchema):
    try:
        product = service.get_product_by_id(product_id)
        updated_product = service.update_product(product.id, payload)
        return product_to_schema(updated_product)
    except NotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
    except Exception as exc:
        logger.error(f"Unexpected error on PATCH /products/{product_id}: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


@products_router.patch(
    "{product_id}/activation",
    response={
        HTTPStatus.OK: ProductSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
    },
)
def product_activation(request, product_id: UUID, payload: ProductActivationSchema):
    try:
        product = service.product_activation(product_id, payload)
        return product_to_schema(product)
    except NotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
    except Exception as exc:
        logger.error(
            f"Unexpected error on PATCH /products/{product_id}/activation: {str(exc)}"
        )
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))


@products_router.delete(
    "/{product_id}",
    response={
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: ErrorSchema,
    },
)
def delete_product(request, product_id: UUID):
    try:
        service.delete_product(product_id)
        return HTTPStatus.NO_CONTENT, None
    except NotFoundError as exc:
        raise HttpError(HTTPStatus.NOT_FOUND, str(exc))
    except Exception as exc:
        logger.error(f"Unexpected error on DELETE /products/{product_id}: {str(exc)}")
        traceback.print_exc()
        raise HttpError(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
