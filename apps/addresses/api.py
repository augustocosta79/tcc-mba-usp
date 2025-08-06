from http import HTTPStatus
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
        HTTPStatus.CONFLICT: ErrorSchema
    },
)
def create_address(request, payload: AddressCreateSchema):
    try:
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
    except UnprocessableEntityError as exc:
        raise
