from fastapi import Request, status
from fastapi.responses import ORJSONResponse


async def unknown_exception_handler(request: Request, err: Exception) -> ORJSONResponse:
    return ORJSONResponse(
        content=dict(msg="Unhandled error"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def setup_exception_handlers(app):
    app.add_exception_handler(Exception, unknown_exception_handler)
