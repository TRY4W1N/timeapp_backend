from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from pymongo.errors import ServerSelectionTimeoutError

from src.domain.common.exception.base import (
    AuthError,
    DomainError,
    EntityNotCreated,
    EntityNotFound,
)


def _make_response(
    status_code: int, err: Exception | None = None, error_type: str | None = None, msg: str | None = None
) -> ORJSONResponse:
    if err is not None:
        content = dict(error_type=err.__class__.__name__, msg=str(err))
    if error_type is not None and msg is not None:
        content = dict(error_type=error_type, msg=msg)
    return ORJSONResponse(content=content, status_code=status_code)


async def database_exception_handler(request: Request, err: ServerSelectionTimeoutError) -> ORJSONResponse:
    return _make_response(
        error_type="Database", msg="Database is unavailable", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


async def entity_exception_handler(request: Request, err: EntityNotCreated | EntityNotFound) -> ORJSONResponse:
    if isinstance(err, EntityNotCreated):
        status_code = status.HTTP_400_BAD_REQUEST
    elif isinstance(err, EntityNotFound):
        status_code = status.HTTP_404_NOT_FOUND
    return _make_response(err=err, status_code=status_code)


async def domain_base_exception_handler(request: Request, err: DomainError) -> ORJSONResponse:
    return _make_response(err=err, status_code=status.HTTP_400_BAD_REQUEST)


async def auth_exception_handler(request: Request, err: AuthError) -> ORJSONResponse:
    return _make_response(err=err, status_code=status.HTTP_401_UNAUTHORIZED)


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    return _make_response(
        error_type="Unknown", msg="Unhandled error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def setup_exception_handlers(app):
    app.add_exception_handler(EntityNotFound, entity_exception_handler)
    app.add_exception_handler(EntityNotCreated, entity_exception_handler)
    app.add_exception_handler(AuthError, auth_exception_handler)
    app.add_exception_handler(DomainError, domain_base_exception_handler)
    app.add_exception_handler(ServerSelectionTimeoutError, database_exception_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)
