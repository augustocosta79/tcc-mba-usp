from ninja import NinjaAPI, Redoc
from http import HTTPStatus
from apps.shared.exceptions.exceptions import NotFoundError, ConflictError, UnauthorizedError, UnprocessableEntityError, OutOfStockError
from utils.logger import configure_logger
from utils.jwt import JWTAuth

from apps.authentication.api import authentication_router
from apps.users.api import users_router
from apps.healthz.api import healthz_router
from apps.products.api import products_router
from apps.categories.api import categories_router
from apps.addresses.api import address_router
from apps.carts.api import cart_router
from apps.orders.api import orders_router

api = NinjaAPI(
    csrf=False,
    title="API",
    version="1.0.0",
    description="This is a API to manage data",
    # auth=JWTAuth()
)


api.add_router("/auth", authentication_router, tags=["Authentication"])
api.add_router("/users", users_router, tags=["Users"])
api.add_router("/healthz", healthz_router, tags=["Healthz"])
api.add_router("/products", products_router, tags=["Products"])
api.add_router("/categories", categories_router, tags=["Categories"])
api.add_router("/addresses", address_router, tags=["Addresses"])
api.add_router("/carts", cart_router, tags=["Carts"])
api.add_router("/orders", orders_router, tags=["Orders"])

# Exception Handlers
logger = configure_logger("api")

api.exception_handler(Exception)
def generic_exception_handler(request, exc: Exception):
    logger.error(
        f"Unhandled exception on {request.method} {request.path}: {exc}",
        exc_info=True  # mostra stack trace completo
    )
    return api.create_response(
        request,
        {"message": "Internal server error"},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

@api.exception_handler(NotFoundError)
def not_found_handler(request, exc: NotFoundError):
    return api.create_response(
        request,
        {"message": str(exc)},
        status=HTTPStatus.NOT_FOUND,
    )

@api.exception_handler(ConflictError)
def conflict_handler(request, exc: ConflictError):
    return api.create_response(
        request,
        {"message": str(exc)},
        status=HTTPStatus.CONFLICT,
    )

@api.exception_handler(UnauthorizedError)
def unauthorized_handler(request, exc: UnauthorizedError):
    return api.create_response(
        request,
        {"message": str(exc)},
        status=HTTPStatus.UNAUTHORIZED,
    )

@api.exception_handler(UnprocessableEntityError)
def unprocessable_entity_handler(request, exc: UnprocessableEntityError):
    return api.create_response(
        request,
        {"message": str(exc)},
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


@api.exception_handler(OutOfStockError)
def out_of_stock_handler(request, exc: OutOfStockError):
    return api.create_response(
        request,
        {"message": str(exc)},
        status=HTTPStatus.CONFLICT,
    )

