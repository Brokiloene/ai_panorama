from aio_pika import ExchangeType

import os
from dotenv import load_dotenv
load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_ADDR = os.getenv("RABBITMQ_ADDR")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:{RABBITMQ_PORT}"
print("================================", RABBITMQ_URL)

EXCHANGE_NAME = "rpc_exchange"
EXCHANGE_TYPE = ExchangeType.DIRECT
RESPONSE_QUEUE = "client_responses"

ROUTING_KEY_TITLE = "gen.title"
ROUTING_KEY_ARTICLE = "gen.article"
ROUTING_KEY_IMAGE = "gen.image"
