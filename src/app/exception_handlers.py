from typing import Any, Callable, Type

from config.system import logger
from exceptions import (
    AiAPITimeoutError,
    DatabaseConnectionError,
    DatabaseNotFoundError,
    S3LoadError,
    S3NotFoundError,
    ViewTemplateNotFoundError,
)
from fastapi import status
from fastapi.responses import JSONResponse


async def internal_server_error_handler(exc: Exception):
    logger.exception("%s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "500 Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


async def s3not_found_error_handler(exc: S3NotFoundError):
    logger.warning("%s", str(exc))
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "404 Not Found",
        },
    )


async def ai_api_timeout_error(exc: AiAPITimeoutError):
    logger.error("Timeout while waiting for %s", exc.action)
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        content="Failed to fetch data from AI. Please try again later",
    )


EXCEPTION_HANDLERS: list[tuple[Type[Any], Callable]] = [
    (S3LoadError, internal_server_error_handler),
    (S3NotFoundError, s3not_found_error_handler),
    (DatabaseNotFoundError, internal_server_error_handler),
    (DatabaseConnectionError, internal_server_error_handler),
    (ViewTemplateNotFoundError, internal_server_error_handler),
    (AiAPITimeoutError, ai_api_timeout_error),
]
