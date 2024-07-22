from fastapi import Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error_type: str
    msg: str


auth_dependencies = [
    Depends(APIKeyHeader(name="Authorization", scheme_name="Authorization", auto_error=True)),
]
response_401 = {
    status.HTTP_401_UNAUTHORIZED: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "example": {"error_type": "AuthError", "msg": "Some problems with auth.."},
            }
        },
    }
}
response_404 = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "example": {"error_type": "EntityNotFound", "msg": "Some entity not found.."},
            }
        },
    }
}
response_400_not_created = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "example": {"error_type": "EntityNotCreated", "msg": "Some entity not created.."},
            }
        },
    }
}
# response_400_not_updated = {
#     status.HTTP_400_BAD_REQUEST: {
#         "model": ErrorSchema,
#         "content": {
#             "application/json": {
#                 "example": {"error_type": "EntityNotUpdated", "msg": "Some entity not updated.."},
#             }
#         },
#     }
# }
response_500 = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorSchema,
        "content": {
            "application/json": {
                "example": {"error_type": "Unknown", "msg": "Unhandled error"},
            }
        },
    }
}
