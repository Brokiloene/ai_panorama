from typing import Mapping

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import Article


class NewsDAO:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.client = mongo_client
        self.db = self.client["ai_panorama"]
        self.collection = self.db["news"]

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
