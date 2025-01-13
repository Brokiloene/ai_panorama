from fastapi import Depends

import app.config as config
from app.dao.news import NewsDAO, NewsDAOFactory
from app.models import Article


news_dao_factory = NewsDAOFactory(config.mongodb.MONGODB_URL)

def get_news_dao() -> NewsDAO:
    global news_dao_factory
    return news_dao_factory.get_news_dao()

