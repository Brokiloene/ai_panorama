import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Response, UploadFile, status
from fastapi.responses import StreamingResponse

from app import config
from app.dao.news import NewsDAO
from app.dependencies import get_news_dao, get_s3_service
from app.models import Article
from app.services import S3Service
from app.views import HTMLTemplate, html_render

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("", status_code=200)
async def get_article(
    start_id: str, response: Response, news_dao: NewsDAO = Depends(get_news_dao)
):
    template_name = HTMLTemplate.LOAD_ARTICLES
    data = await news_dao.read_multiple(start_id, config.html.NEWS_LOAD_BATCH_SIZE)
    if data == []:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        return html_render(template_name, data)


@router.post("")
async def create_article(
    title: Annotated[str, Form()],
    article_text: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    news_dao: NewsDAO = Depends(get_news_dao),
    s3_service: S3Service = Depends(get_s3_service),
):
    object_name = str(uuid.uuid4())
    async with await s3_service.get_s3_client() as client:
        await s3_service.upload_object(
            client,
            image.file,
            config.s3.NEWS_IMGS_BUCKET,
            object_name,
            image.content_type,
        )

    await news_dao.create(
        Article(image_path=object_name, title=title, article_text=article_text)
    )


@router.get("image/{file_key}")
async def get_article_image(
    file_key: str, s3_service: S3Service = Depends(get_s3_service)
):
    async def s3_stream():
        async with await s3_service.get_s3_client() as client:
            data = await s3_service.download_object(
                client, config.s3.NEWS_IMGS_BUCKET, file_key
            )
            yield data.get("ContentType", "application/octet-stream")
            async for chunk in data["Body"]:
                yield chunk

    stream = s3_stream()
    media_type = await anext(stream)
    return StreamingResponse(stream, media_type=media_type)
