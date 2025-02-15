from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient

from .config.mongodb import mongo_config
from .dao.news import NewsDAO
from .services import AIApiService, S3Service


def get_db_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(
        host=mongo_config.host,
        tls=mongo_config.tls,
        tlsCertificateKeyFile=mongo_config.tlsCertificateKeyFile,
        tlsAllowInvalidCertificates=mongo_config.tlsAllowInvalidCertificates,
    )


async def get_s3_service() -> S3Service:
    return S3Service()


async def get_news_dao(
    client: Annotated[AsyncIOMotorClient, Depends(get_db_client)],
) -> NewsDAO:
    news_dao = NewsDAO(client)
    await news_dao.start_connection()
    return news_dao


async def get_ai_api_service(request: Request) -> AIApiService:
    return request.app.state.ai_api_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ai_api_service = AIApiService()
    await app.state.ai_api_service.start_connection()
    yield
    await app.state.ai_api_service.close_connection()
