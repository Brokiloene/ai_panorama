from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient

import app.config as config
from app.dao.news import NewsDAO
from app.services import S3Service, AIApiService


def get_db_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(config.mongodb.MONGODB_URL)


async def get_s3_service() -> S3Service:
    return S3Service()

async def get_news_dao(
        client: Annotated[AsyncIOMotorClient, Depends(get_db_client)]
    ) -> NewsDAO:
    return NewsDAO(client)

async def get_ai_api_service(request: Request) -> AIApiService:
    return request.app.state.ai_api_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ai_api_service = AIApiService()    
    yield
    await app.state.ai_api_service.close_connection()
