from aio_pika import ExchangeType

# RABBITMQ_URL = "amqp://myuser:mypassword@127.0.0.1:5672/"
# RABBITMQ_USER = "myuser"
# RABBITMQ_PASS = "mypassword"
# RABBITMQ_ADDR = "172.17.0.1"
# RABBITMQ_PORT = "5672"

import os
from dotenv import load_dotenv
load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_ADDR = os.getenv("RABBITMQ_ADDR")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

RABBITMQ_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_ADDR}:{RABBITMQ_PORT}"
print("================================", RABBITMQ_URL)
# RABBITMQ_URL = "amqp://myuser:mypassword@172.17.0.1:5672/"

RPC_EXCHANGE_NAME = "rpc_exchange"
EXCHANGE_TYPE = ExchangeType.DIRECT
RESPONSE_QUEUE = "client_responses"

ROUTING_KEY_TITLE = "gen.title"
ROUTING_KEY_ARTICLE = "gen.article"
ROUTING_KEY_IMAGE = "gen.image"
