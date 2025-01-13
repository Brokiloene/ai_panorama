import aiofiles

import asyncio
import logging
import aio_pika
from aio_pika import ExchangeType

# Параметры подключения
RABBITMQ_URL = "amqp://rabbitmqPanoramaAI:rabbitmqPasswordPanoramaAI@http://212.192.246.59:5672"

RPC_EXCHANGE_NAME = "rpc_exchange"
EXCHANGE_TYPE = ExchangeType.DIRECT

QUEUE_TITLE = "title_requests"
QUEUE_ARTICLE = "article_requests"
QUEUE_IMAGE = "image_requests"

ROUTING_KEY_TITLE = "gen.title"
ROUTING_KEY_ARTICLE = "gen.article"
ROUTING_KEY_IMAGE = "gen.image"

RESPONSE_QUEUE = "client_responses"     # Очередь ответов



async def process_title_request(message: aio_pika.abc.AbstractIncomingMessage, exchange: aio_pika.Exchange):
    async with message.process():
        try:
            request_text = message.body.decode()
            logging.info(f" [x] Получен запрос: {request_text}")

            generated_title = "My awesome generated title!"

            response_msg = aio_pika.Message(
                body=generated_title.encode("utf-8"),
                correlation_id=message.correlation_id
            )

            reply_to_queue = message.reply_to
            if reply_to_queue:
                await exchange.publish(response_msg, routing_key=reply_to_queue)
                logging.info(f" [x] Отправлен ответ: exchange='{RPC_EXCHANGE_NAME}', routing_key='{reply_to_queue}'")
            else:
                logging.warning(" [!] Пустой reply_to — не знаем, куда отправлять ответ")

        except Exception as e:
            logging.error(f"Ошибка при обработке: {e}", exc_info=True)


async def process_article_request(message: aio_pika.abc.AbstractIncomingMessage, exchange: aio_pika.Exchange):
    async with message.process():
        try:
            request_text = message.body.decode()
            logging.info(f"[article] Получен запрос: {request_text}")
            logging.info(f"[article] Получен replyto: {message.reply_to}")

            generated_text = "My awesome generated article!"

            response_msg = aio_pika.Message(
                body=generated_text.encode("utf-8"),
                correlation_id=message.correlation_id
            )

            reply_to_queue = message.reply_to
            if reply_to_queue:
                await exchange.publish(
                    response_msg,
                    routing_key=reply_to_queue
                )
                logging.info(f"[article] Отправлен ответ -> {reply_to_queue}")
            else:
                logging.warning("[article] Пустой reply_to — не знаем, куда отправлять ответ")

        except Exception as e:
            logging.error(f"[article] Ошибка при обработке: {e}", exc_info=True)


async def process_image_request(message: aio_pika.abc.AbstractIncomingMessage, exchange: aio_pika.Exchange):
    async with message.process():
        try:
            request_text = message.body.decode()
            logging.info(f"[image] Получен запрос: {request_text}")

            file_path = "src/static/v.png"
            logging.info(f"{file_path}")
            async with aiofiles.open(file_path, "rb") as f:
                data = await f.read()

   
            response_msg = aio_pika.Message(
                body=data,
                correlation_id=message.correlation_id
            )

            reply_to_queue = message.reply_to
            if reply_to_queue:
                await exchange.publish(response_msg, routing_key=reply_to_queue)
                logging.info(f"[image] Отправлен ответ -> {reply_to_queue}")
            else:
                logging.warning("[image] Пустой reply_to")

        except Exception as e:
            logging.error(f"[image] Ошибка при обработке: {e}", exc_info=True)



async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Подключаемся к RabbitMQ...")

    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    channel = await connection.channel()

    exchange = await channel.declare_exchange(
        RPC_EXCHANGE_NAME,
        EXCHANGE_TYPE,
        durable=True
    )

    # 4. Объявляем очередь для запросов (REQUEST_QUEUE) и биндим её к exchange
    queue_title = await channel.declare_queue(QUEUE_TITLE, durable=True)
    await queue_title.bind(exchange, routing_key=ROUTING_KEY_TITLE)

    logging.info(f"Подписываемся на очередь '{QUEUE_TITLE}' и ждём сообщений...")

    # 5. Подписываемся, передавая exchange как аргумент в колбэк
    await queue_title.consume(
        lambda message: process_title_request(message, exchange)
    )

    queue_article = await channel.declare_queue(QUEUE_ARTICLE, durable=True)
    await queue_article.bind(exchange, routing_key=ROUTING_KEY_ARTICLE)
    logging.info(f"Подписываемся на очередь '{QUEUE_ARTICLE}' и ждём сообщений...")
    await queue_article.consume(
        lambda message: process_article_request(message, exchange)
    )

    queue_image = await channel.declare_queue(QUEUE_IMAGE, durable=True)
    await queue_image.bind(exchange, routing_key=ROUTING_KEY_IMAGE)
    logging.info(f"Подписываемся на очередь '{QUEUE_IMAGE}' и ждём сообщений...")
    await queue_image.consume(
        lambda message: process_image_request(message, exchange)
    )


    # 6. Чтобы программа не завершилась, «зависаем» в event loop
    try:
        await asyncio.Future()  # Задача, которая не завершится сама по себе
    except KeyboardInterrupt:
        logging.info("Остановка по Ctrl+C ...")
    finally:
        await channel.close()
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
