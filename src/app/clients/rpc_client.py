import uuid
import logging
import asyncio
import aio_pika


class RPCClient:
    def __init__(
        self,
        exchange: aio_pika.Exchange,
        response_queue: aio_pika.Queue,
        pending_futures: dict
    ):
        self.exchange = exchange
        self.response_queue = response_queue
        self.pending_futures = pending_futures

    async def rpc_request(
        self,
        message_body: bytes,
        routing_key: str,
        timeout: float = 5.0
    ) -> bytes:
        """
        Публикует сообщение с указанным `routing_key` в exchange,
        указывает reply_to = self.response_queue.name,
        ждёт ответ (через correlation_id) или падает по таймауту.
        Возвращает байты ответа.
        """
        correlation_id = str(uuid.uuid4())
        loop = asyncio.get_running_loop()

        future = loop.create_future()
        self.pending_futures[correlation_id] = future

        msg = aio_pika.Message(
            body=message_body,
            correlation_id=correlation_id,
            reply_to=self.response_queue.name
        )

        await self.exchange.publish(msg, routing_key=routing_key)
        logging.info(f"[x] Sent RPC request (corr_id={correlation_id}) via '{routing_key}'")

        try:
            body = await asyncio.wait_for(future, timeout=timeout)
            return body
        except asyncio.TimeoutError:
            self.pending_futures.pop(correlation_id, None)
            raise TimeoutError("RPC request timed out")

