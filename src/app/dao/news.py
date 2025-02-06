from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.models import Article


class NewsDAO:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.client = mongo_client
        self.db = self.client["ai_panorama"]
        self.collection = self.db["news"]

    async def create(self, item: Article):
        await self.collection.insert_one(item.model_dump())
    
    async def read_multiple(self, start_id: str|None, amount: int):
        if start_id is None:
            start_doc = await self.collection.find_one(sort=[("_id", 1)])
            start_id = start_doc["_id"]
            query = {"_id": {"$gte": ObjectId(start_id)}}
        else:
            query = {"_id": {"$gt": ObjectId(start_id)}}
        res = await self.collection.find(query).sort("_id", 1).limit(amount).to_list(length=amount)
        return res
    
    async def count_news(self):
        res = await self.collection.count_documents({})
        return res
