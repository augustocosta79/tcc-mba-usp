from http import HTTPStatus
from typing import List
from uuid import UUID

from apps.carts.repository import CartRepository
from apps.carts.schema import (
    AddToCartSchema,
    CartSchema,
    SubtractCartItemQuantitySchema,
)
from apps.carts.serializers import cart_entity_to_schema
from apps.carts.service import CartService
from apps.products.repository import ProductRepository
from apps.products.service import ProductService
from apps.users.repository import UserRepository
from apps.users.service import UserService
from ninja import Router
from utils.error_schema import ErrorSchema
from utils.logger import configure_logger

cart_router = Router()

logger = configure_logger(__name__)

user_repository = UserRepository()
user_service = UserService(user_repository, logger)

product_repository = ProductRepository()
product_service = ProductService(product_repository, logger)

repository = CartRepository()
service = CartService(repository, product_service, user_service, logger)


@cart_router.post(
    "/{user_id}/add",
    response={
        HTTPStatus.OK: CartSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def add_to_cart(request, user_id: UUID, payload: AddToCartSchema):
    cart = service.add_to_cart(user_id, payload.product_id, payload.quantity)
    return cart_entity_to_schema(cart)


@cart_router.post(
    "/{user_id}/subtract",
    response={
        HTTPStatus.OK: CartSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def subtract_quantity_from_cart_item(
    request, user_id: UUID, payload: SubtractCartItemQuantitySchema
):
    cart = service.subtract_quantity_from_cart_item(
        user_id, payload.product_id, payload.quantity
    )
    return cart_entity_to_schema(cart)
