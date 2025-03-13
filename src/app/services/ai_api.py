import asyncio
import uuid

import aio_pika

from app import config
from app.config.app import logger


class AIApiService:
    def __init__(self):
        self.pending_requests: dict[str, asyncio.Future] = {}
        self.connection: aio_pika.abc.AbstractRobustConnection
        self.channel: aio_pika.abc.AbstractChannel
        self.exchange: aio_pika.abc.AbstractExchange
        self.response_queue: aio_pika.abc.AbstractQueue

    async def start_connection(self):
        self.connection = await aio_pika.connect_robust(config.rabbitmq.URL)
        self.channel = await self.connection.channel()
        self.exchange = await self.channel.declare_exchange(
            config.rabbitmq.EXCHANGE_NAME, config.rabbitmq.EXCHANGE_TYPE, durable=True
        )
        self.response_queue = await self.channel.declare_queue(
            config.rabbitmq.RESPONSE_QUEUE, durable=True
        )
        await self.response_queue.bind(
            self.exchange, routing_key=config.rabbitmq.RESPONSE_QUEUE
        )

        def on_response(message: aio_pika.abc.AbstractIncomingMessage):
            corr_id = message.correlation_id
            if not corr_id:
                logger.warning("RabbitMQ returned message without corr_id")
                return

            future = self.pending_requests.pop(corr_id, None)
            if future and not future.done():
                future.set_result(message.body)

        await self.response_queue.consume(on_response, no_ack=True)
        logger.info("[x] Subscribed to response queue")

    async def close_connection(self):
        await self.channel.close()
        await self.connection.close()
        logger.info("RabbitMQ connection closed")

    async def send_request(
        self, message_body: bytes, routing_key: str, timeout: float = 5.0
    ) -> bytes:
        """
        Публикует сообщение с указанным `routing_key` в exchange,
        возвращает ответ или падает по таймауту (в секундах).

        :raises: `TimeoutError`
        """
        correlation_id = str(uuid.uuid4())
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        self.pending_requests[correlation_id] = future

        msg = aio_pika.Message(
            body=message_body,
            correlation_id=correlation_id,
            reply_to=self.response_queue.name,
        )

        await self.exchange.publish(msg, routing_key=routing_key)
        logger.info(
            "[x] Sent AI API request (corr_id=%s) via '%s'", correlation_id, routing_key
        )

        try:
            body = await asyncio.wait_for(future, timeout=timeout)
        except asyncio.TimeoutError as exc:
            self.pending_requests.pop(correlation_id, None)
            logger.warning(
                "AI API request (corr_id=%s) via '%s' timed out",
                correlation_id,
                routing_key,
            )
            raise TimeoutError("AI API request timed out") from exc
        return body
