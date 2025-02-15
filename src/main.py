import uuid
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, File, Form, Query, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.config.system import logger
from app.dao.news import NewsDAO
from app.dependencies import get_ai_api_service, get_news_dao, get_s3_service, lifespan
from app.exception_handlers import EXCEPTION_HANDLERS
from app.exceptions import AiAPITimeoutError
from app.models import Article
from app.services import AIApiService, S3Service
from app.views import html_render

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    f"/{config.system.STATIC_FILES_DIR}",
    StaticFiles(directory=config.system.STATIC_FILES_DIR),
    name="static",
)

for exc_cls, handler in EXCEPTION_HANDLERS:
    app.add_exception_handler(exc_cls, handler)


@app.get("/", response_class=HTMLResponse)
async def get_root(news_dao: NewsDAO = Depends(get_news_dao)):
    template_name = "index.jinja"
    data = await news_dao.read_multiple(None, config.html.NEWS_LOAD_BATCH_SIZE)
    return html_render(template_name, data)


@app.get("/get-news/", status_code=200)
async def get_news(
    start_id: str, response: Response, news_dao: NewsDAO = Depends(get_news_dao)
):
    template_name = "form_news.jinja"
    data = await news_dao.read_multiple(start_id, config.html.NEWS_LOAD_BATCH_SIZE)
    if data == []:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        return html_render(template_name, data)


@app.get("/image/{file_key}")
async def get_image(file_key: str, s3_service: S3Service = Depends(get_s3_service)):
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


@app.post("/add-article")
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


@app.get("/gen-title/", response_class=Response)
async def gen_title(
    prompt: str = Query(), ai_api_service: AIApiService = Depends(get_ai_api_service)
):
    try:
        response_body = await ai_api_service.send_request(
            message_body=bytes(prompt, encoding="utf-8"),
            routing_key=config.rabbitmq.ROUTING_KEY_TITLE,
            timeout=5.0,
        )
    except TimeoutError:
        raise AiAPITimeoutError("article headline generation") from None
    text_response = response_body.decode("utf-8")
    logger.info("Got generated article headline: %s", text_response)
    return Response(content=text_response, media_type="text/plain")


@app.get("/gen-article/", response_class=Response)
async def gen_article(
    prompt: str = Query(), ai_api_service: AIApiService = Depends(get_ai_api_service)
):
    try:
        response_body = await ai_api_service.send_request(
            message_body=bytes(prompt, encoding="utf-8"),
            routing_key=config.rabbitmq.ROUTING_KEY_ARTICLE,
            timeout=10.0,
        )
    except TimeoutError:
        raise AiAPITimeoutError("article body generation") from None

    text_response = response_body.decode("utf-8")
    logger.info("Got generated article body: %s", text_response)
    return Response(content=text_response, media_type="text/plain")


@app.get("/gen-image/", response_class=Response)
async def gen_image(
    prompt: str = Query(), ai_api_service: AIApiService = Depends(get_ai_api_service)
):
    try:
        response_body = await ai_api_service.send_request(
            message_body=bytes(prompt, encoding="utf-8"),
            routing_key=config.rabbitmq.ROUTING_KEY_IMAGE,
            timeout=30.0,
        )
    except TimeoutError:
        raise AiAPITimeoutError("article thumbnail generation") from None

    return Response(content=response_body, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        ssl_certfile=config.system.TLS_CERTIFICATE,
        ssl_keyfile=config.system.TLS_PRIVATE_KEY,
        ssl_ciphers="TLSv1",
    )
