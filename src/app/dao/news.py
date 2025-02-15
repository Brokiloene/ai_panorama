from typing import Mapping

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import mongodb
from app.exceptions import DatabaseConnectionError, DatabaseNotFoundError
from app.models import Article


class NewsDAO:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        """
        :raises: `DatabaseNotFoundError`
        :raises: `DatabaseConnectionError`
        """
        self.client = mongo_client
        if not self.db_exists():
            raise DatabaseNotFoundError(
                "Could not connect to MongoDB database with name" f"{mongodb.DB_NAME}"
            )
        self.db = self.client[mongodb.DB_NAME]
        if not self.collection_exists():
            raise DatabaseConnectionError(
                "Could not get MongoDB collection with name"
                f"{mongodb.NEWS_COLLECTION_NAME}"
            )

        self.collection = self.db[mongodb.NEWS_COLLECTION_NAME]

    async def db_exists(self) -> bool:
        db_names = await self.client.list_database_names()
        return mongodb.DB_NAME in db_names

    async def collection_exists(self) -> bool:
        collection_names = await self.db.list_collection_names()
        return mongodb.NEWS_COLLECTION_NAME in collection_names

    async def create(self, item: Article):
        await self.collection.insert_one(item.model_dump())

    async def read_multiple(self, start_id: str | None, amount: int) -> list[Article]:
        """
        Считывает `amount`
        """
        if start_id is None:
            start_doc = await self.collection.find_one(sort=[("_id", 1)])
            if start_doc is None:
                return []
            start_id = start_doc["_id"]
            query = {"_id": {"$gte": ObjectId(start_id)}}
        else:
            query = {"_id": {"$gt": ObjectId(start_id)}}
        data: list[Mapping] = (
            await self.collection.find(query)
            .sort("_id", 1)
            .limit(amount)
            .to_list(length=amount)
        )
        res: list[Article] = [Article(**x) for x in data]
        return res

    async def count_news(self) -> int:
        res = await self.collection.count_documents({})
        return res
