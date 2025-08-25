from uuid import UUID
from ninja import Router
from utils.error_schema import ErrorSchema
from utils.logger import configure_logger
from http import HTTPStatus
from apps.orders.service import OrderService
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
from apps.orders.schemas import OrderSchema, OrderCreateSchema


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
