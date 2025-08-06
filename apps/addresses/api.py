from http import HTTPStatus
from uuid import UUID
from ninja import Router
from apps.addresses.schema import AddressSchema, AddressCreateSchema
from apps.addresses.service import AddressService
from apps.addresses.repository import AddressRepository
from utils.logger import configure_logger
from apps.users.service import UserService
from apps.users.repository import UserRepository
from apps.addresses.serializers import from_address_entity_to_schema
from apps.shared.exceptions import UnprocessableEntityError
from utils.error_schema import ErrorSchema

address_router = Router()
logger = configure_logger(__name__)
address_repository = AddressRepository()
user_repository = UserRepository()
user_service = UserService(user_repository, logger)

service = AddressService(address_repository, logger, user_service)


@address_router.post(
    "",
    response={
        HTTPStatus.CREATED: AddressSchema,
        HTTPStatus.UNPROCESSABLE_ENTITY: ErrorSchema,
        HTTPStatus.CONFLICT: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_address(request, payload: AddressCreateSchema):
    address = service.create_address(
        payload.user_id,
        payload.street,
        payload.street_number,
        payload.complement,
        payload.district,
        payload.city,
        payload.state_code,
        payload.postal_code,
        payload.country,
        payload.is_default,
    )
    return HTTPStatus.CREATED, from_address_entity_to_schema(address)


@address_router.get(
    "/{address_id}",
    response={
        HTTPStatus.OK: AddressSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def get_address(request, address_id: str):
    address = service.get_address_by_id(address_id)
    return from_address_entity_to_schema(address)


@address_router.get(
    "/user/{user_id}",
    response={
        HTTPStatus.OK: list[AddressSchema],
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def list_addresses_for(request, user_id: UUID):
    addresses = service.list_addresses_for(user_id)
    return [
        from_address_entity_to_schema(address)
        for address in addresses
    ]

@address_router.delete(
    "/{address_id}",
    response = {
        HTTPStatus.NO_CONTENT: None,
        HTTPStatus.NOT_FOUND: ErrorSchema
    }
)
def delete_address(request, address_id: UUID):
    service.delete_address(address_id)
    return HTTPStatus.NO_CONTENT, None