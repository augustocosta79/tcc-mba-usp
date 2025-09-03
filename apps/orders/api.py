from uuid import UUID
from ninja import Router, Query
from utils.error_schema import ErrorSchema
from utils.logger import configure_logger
from http import HTTPStatus
from apps.orders.service import OrderService
from apps.orders.enums import OrderStatus
from apps.orders.repository import OrderRepository
from apps.products.service import ProductService
from apps.products.repository import ProductRepository
from apps.categories.service import CategoryService
from apps.categories.repository import CategoryRepository
from apps.addresses.service import AddressService
from apps.addresses.repository import AddressRepository
from apps.carts.service import CartService
from apps.carts.repository import CartRepository
from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.orders.schemas import OrderSchema, OrderCreateSchema, OrderStatusChangeSchema, OrderItemQuantityChangeSchema


logger = configure_logger(__name__)
user_service = UserService(UserRepository(), logger)
product_service = ProductService(ProductRepository(), logger)
category_service = CategoryService(CategoryRepository(), logger)
address_service = AddressService(AddressRepository(), logger)
cart_service = CartService(CartRepository(), product_service, user_service, logger)

service = OrderService(OrderRepository(), user_service, product_service, cart_service, address_service)


orders_router = Router()


@orders_router.post(
    "/users/{user_id}",
    response={
        HTTPStatus.CREATED: OrderSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_order(request, user_id: UUID, payload: OrderCreateSchema):
    return HTTPStatus.CREATED, service.create_order(user_id, payload.address_id)


@orders_router.get(
    "/{order_id}",
    response = {
        HTTPStatus.OK: OrderSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema
    }
)
def get_order_by_id(request, order_id: UUID) -> OrderSchema:
    return service.get_order_by_id(order_id)


@orders_router.get(
    "",
    response={
        HTTPStatus.OK: list[OrderSchema],
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    }
)
def list_orders_by_user(request, user_id: UUID = Query(...)):
    return service.list_orders_by_user_id(user_id)


@orders_router.patch(
    "/{order_id}/status",
    response = {
        HTTPStatus.OK: OrderSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    }
)
def set_order_status(request, order_id: UUID, payload: OrderStatusChangeSchema):
    return service.set_status(order_id, payload.new_status)


@orders_router.delete(
    "/{order_id}/items/{item_id}",
    response = {
        HTTPStatus.OK: OrderSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    }
)
def delete_order_item(request, order_id: UUID, item_id: UUID) -> OrderSchema:
    return service.remove_item_from_order(order_id, item_id)

@orders_router.patch(
    "/{order_id}/cancel",
    response = {
        HTTPStatus.OK: OrderSchema,
        HTTPStatus.CONFLICT: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
    }
)
def cancel_order(request, order_id: UUID):
    return service.cancel_order(order_id)

@orders_router.post(
    "/{order_id}/items/{item_id}",
    response = {
        HTTPStatus.OK: OrderSchema,
        HTTPStatus.CONFLICT: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema
    }
)
def change_order_item_quantity(request, order_id: UUID, item_id: UUID, payload: OrderItemQuantityChangeSchema):
    operations = {
        "increase": service.increase_order_item_quantity,
        "decrease": service.decrease_order_item_quantity
    }
    return operations[payload.operation.value](order_id, item_id, payload.quantity)