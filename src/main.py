from typing import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Form, Response, status, Depends, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import aio_pika

import app.config as config
from app.config.system import logger
from app.views.html_view import html_view
from app.dao.news import NewsDAO
from app.dependencies import get_news_dao, news_dao_factory
from app.models import Article
from app.clients.rpc_client import RPCClient
from app.services.save_image import save_image_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    connection = await aio_pika.connect_robust(config.rabbitmq.RABBITMQ_URL)
    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        config.rabbitmq.RPC_EXCHANGE_NAME, 
        config.rabbitmq.EXCHANGE_TYPE, 
        durable=True
    )

    response_queue = await channel.declare_queue(config.rabbitmq.RESPONSE_QUEUE, durable=True)
    await response_queue.bind(exchange, routing_key=config.rabbitmq.RESPONSE_QUEUE)

    pending_futures = {}

    def on_response(message: aio_pika.abc.AbstractIncomingMessage):
        corr_id = message.correlation_id
        if not corr_id:
            return

        future = pending_futures.pop(corr_id, None)
        if future and not future.done():
            future.set_result(message.body)

    await response_queue.consume(on_response, no_ack=True)
    logger.info("[x] Subscribed to response queue")

    app.state.rpc_client = RPCClient(
        exchange=exchange,
        response_queue=response_queue,
        pending_futures=pending_futures,
    )

    try:
        yield
    finally:
        await channel.close()
        await connection.close()

        await news_dao_factory.client.close()



app = FastAPI(lifespan=lifespan)
# app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(f"/{config.system.STATIC_FILES_DIR}", StaticFiles(directory=config.system.STATIC_FILES_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def get_root(news_dao: NewsDAO = Depends(get_news_dao)):
    template_name = "index.jinja"
    data = await news_dao.read_multiple(None, config.html.NEWS_LOAD_BATCH_SIZE)
    return html_view(template_name, data)


@app.get("/get-news/", status_code=200)
async def get_news(start_id: str, response: Response, news_dao: NewsDAO = Depends(get_news_dao)):
    template_name = "form_news.jinja"
    data = await news_dao.read_multiple(start_id, 9)
    if data == []:
        response.status_code = status.HTTP_204_NO_CONTENT
    else:
        return html_view(template_name, data)


@app.post("/add-article")
async def create_article(
    title: Annotated[str, Form()],
    article_text: Annotated[str, Form()],
    image: Annotated[UploadFile, File()],
    news_dao: NewsDAO = Depends(get_news_dao)
):
    news_cnt = await news_dao.count_news()
    filename = str(news_cnt)
    image_path = await save_image_service(await image.read(), filename)
    await news_dao.create(Article(image_path=image_path, title=title, article_text=article_text))


@app.get("/gen-title/", response_class=Response)
async def gen_title(prompt: str = Query()):
    try:
        response_body = await app.state.rpc_client.rpc_request(
            message_body=bytes(prompt, encoding='utf-8'),
            routing_key=config.rabbitmq.ROUTING_KEY_TITLE,
            timeout=5.0
        )
    except TimeoutError:
        logger.error("Timeout while waiting for RPC response")
        return Response(content="Failed to fetch title (timeout)", status_code=500)
    text_response = response_body.decode('utf-8')
    logger.info(f"[x] Got generated title: {text_response}")
    return Response(content=text_response, media_type="text/plain")


@app.get("/gen-article/", response_class=Response)
async def gen_article(prompt: str = Query()):
    try:
        response_body = await app.state.rpc_client.rpc_request(
            message_body=bytes(prompt, encoding='utf-8'),
            routing_key=config.rabbitmq.ROUTING_KEY_ARTICLE,
            timeout=5.0
        )
    except TimeoutError:
        logger.error("Timeout while waiting for article")
        return Response(content="Failed to fetch article (timeout)", status_code=500)

    text_response = response_body.decode('utf-8')
    logger.info(f"[x] Got generated article: {text_response}")
    return Response(content=text_response, media_type="text/plain")


@app.get("/gen-image/", response_class=Response)
async def gen_image(prompt: str = Query()):
    try:
        response_body = await app.state.rpc_client.rpc_request(
            message_body=bytes(prompt, encoding='utf-8'),
            routing_key=config.rabbitmq.ROUTING_KEY_IMAGE,
            timeout=5.0
        )
    except TimeoutError:
        logger.error("Timeout while waiting for image")
        return Response(content="Failed to fetch image (timeout)", status_code=500)
    
    logger.info("[x] Got image response")
    return Response(content=response_body, media_type="image/png")


if __name__ == '__main__':
    # uvicorn.run("main:app", reload=True, log_config=None)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
    