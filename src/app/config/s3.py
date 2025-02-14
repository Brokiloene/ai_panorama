import os
from typing import NamedTuple

from dotenv import load_dotenv

from app.config import system

load_dotenv()

ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "")
SECRET_KEY = os.getenv("S3_SECRET_KEY", "")
ADDR = os.getenv("S3_ADDR", "")
PORT = os.getenv("S3_PORT", "")
URL = f"https://{ADDR}:{PORT}"
NEWS_IMGS_BUCKET = os.getenv("NEWS_IMGS_BUCKET", "")


class S3Config(NamedTuple):
    service_name: str
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    verify: str


s3_config = S3Config(
    service_name="s3",
    endpoint_url=URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    verify=system.TLS_CERTIFICATE,
)
