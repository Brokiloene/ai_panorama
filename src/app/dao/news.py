from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from app.models import Article


class NewsDAO:
    def __init__(self, mongo_client: AsyncIOMotorClient):
        self.mongo_client = mongo_client
        self.db = self.mongo_client["news_testing"]
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

class NewsDAOFactory:
    def __init__(self, mongodb_url: str):
        self.client = AsyncIOMotorClient(mongodb_url)
    def get_news_dao(self) -> NewsDAO:
        return NewsDAO(mongo_client=self.client)

# class NewsDAO:
#     def __init__(self, data: list):
#         self.data: list[Article] = data
    
#     def create(self, item: Article):
#         item.id = len(self.data)
#         self.data.append(item)

#     def read_by_id(self, article_id: int) -> Article|None:
#         for article in self.data:
#             if article.id == article_id:
#                 return article
#         return None
    
#     def read_batch(self, start_id: int) -> list[Article]:
#         if self.count() < start_id:
#             return []
#         return self.data[start_id:start_id+9]
    
#     def delete(self, article_id: int):
#         self.data.pop(article_id)
    
#     def count(self):
#         return len(self.data)

