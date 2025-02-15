from fastapi import APIRouter, Depends, Query, Response

from app import config
from app.config.app import logger
from app.dependencies import get_ai_api_service
from app.exceptions import AiAPITimeoutError
from app.services import AIApiService

router = APIRouter(prefix="/ai-gen", tags=["AI API"])


@router.get("/article-headline", response_class=Response)
async def ai_gen_article_headline(
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


@router.get("/article-body", response_class=Response)
async def ai_gen_article_body(
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


@router.get("/article-thumbnail", response_class=Response)
async def ai_gen_article_tnumbnail(
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
