from typing import Any, Callable, Type

from config.system import logger
from exceptions import (
    DatabaseConnectionError,
    DatabaseNotFoundError,
    S3LoadError,
    S3NotFoundError,
    ViewTemplateNotFoundError,
)
from fastapi import status
from fastapi.responses import JSONResponse


async def s3load_error_handler(exc: S3LoadError):
    logger.exception("%s", str(exc))
    return JSONResponse(
        content={
            "error": "500 Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def s3not_found_error_handler(exc: S3NotFoundError):
    logger.warning("%s", str(exc))
    return JSONResponse(
        content={
            "error": "404 Not Found",
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


async def db_not_found_error_handler(exc: DatabaseNotFoundError):
    logger.exception("%s", str(exc))
    return JSONResponse(
        content={
            "error": "500 Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def db_connection_error_handler(exc: DatabaseConnectionError):
    logger.exception("%s", str(exc))
    return JSONResponse(
        content={
            "error": "500 Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def view_template_not_found_error_handler(exc: ViewTemplateNotFoundError):
    logger.exception("%s", str(exc))
    return JSONResponse(
        content={
            "error": "500 Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


EXCEPTION_HANDLERS: list[tuple[Type[Any], Callable]] = [
    (S3LoadError, s3load_error_handler),
    (S3NotFoundError, s3not_found_error_handler),
    (DatabaseNotFoundError, db_not_found_error_handler),
    (DatabaseConnectionError, db_connection_error_handler),
    (ViewTemplateNotFoundError, view_template_not_found_error_handler),
]
