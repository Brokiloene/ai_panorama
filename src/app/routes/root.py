from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app import config
from app.dao.news import NewsDAO
from app.dependencies import get_news_dao
from app.views import HTMLTemplate, html_render

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_root(news_dao: NewsDAO = Depends(get_news_dao)):
    template_name = HTMLTemplate.INDEX
    data = await news_dao.read_multiple(None, config.html.NEWS_LOAD_BATCH_SIZE)
    return html_render(template_name, data)
