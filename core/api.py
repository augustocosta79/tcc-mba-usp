from ninja import NinjaAPI, Redoc
from http import HTTPStatus
from apps.shared.exceptions.exceptions import NotFoundError, ConflictError, UnauthorizedError

from apps.authentication.api import authentication_router
from apps.users.api import users_router
from apps.healthz.api import healthz_router
from apps.products.api import products_router

api = NinjaAPI(
    csrf=False,
    title="API",
    version="1.0.0",
    description="This is a API to manage data",
)


api.add_router("/auth", authentication_router, tags=["Authentication"])
api.add_router("/users", users_router, tags=["Users"])
api.add_router("/healthz", healthz_router, tags=["Healthz"])
api.add_router("/products", products_router, tags=["Products"])

# Exception Handlers
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
