import os

from aio_pika import ExchangeType
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("RABBITMQ_USER")
PASS = os.getenv("RABBITMQ_PASS")
ADDR = os.getenv("RABBITMQ_ADDR")
PORT = os.getenv("RABBITMQ_PORT")

URL = f"amqp://{USER}:{PASS}@{ADDR}:{PORT}"

EXCHANGE_NAME = "rpc_exchange"
EXCHANGE_TYPE = ExchangeType.DIRECT
RESPONSE_QUEUE = "client_responses"

ROUTING_KEY_TITLE = "gen.title"
ROUTING_KEY_ARTICLE = "gen.article"
ROUTING_KEY_IMAGE = "gen.image"
