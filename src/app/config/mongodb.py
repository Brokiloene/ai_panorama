import os
from typing import NamedTuple

from dotenv import load_dotenv

from app.config import app

load_dotenv()

USER = os.getenv("MONGODB_USER")
PASS = os.getenv("MONGODB_PASS")
ADDR = os.getenv("MONGODB_ADDR")
PORT = os.getenv("MONGODB_PORT")

URL = f"mongodb://{USER}:{PASS}@{ADDR}:{PORT}/?tls=true"


class MongoConfig(NamedTuple):
    host: str
    tls: bool
    tlsCertificateKeyFile: str
    tlsAllowInvalidCertificates: bool


mongo_config: MongoConfig = MongoConfig(
    host=URL,
    tls=True,
    tlsCertificateKeyFile=app.TLS_COMBINED_CERT,
    tlsAllowInvalidCertificates=True,
)

DB_NAME = "ai_panorama"
NEWS_COLLECTION_NAME = "news"
