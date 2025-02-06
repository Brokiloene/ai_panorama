import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY    = os.getenv("S3_ACCESS_KEY")
SECRET_KEY    = os.getenv("S3_SECRET_KEY")
ADDR          = os.getenv("S3_ADDR")
PORT          = os.getenv("S3_PORT")
URL           = f"https://{ADDR}:{PORT}"
NEWS_IMGS_BUCKET = os.getenv("NEWS_IMGS_BUCKET")

import app.config.system as system

client_config = {
    "service_name": "s3",
    "endpoint_url": URL,
    "aws_access_key_id": ACCESS_KEY,
    "aws_secret_access_key": SECRET_KEY,
    "verify": system.TLS_CERTIFICATE
}
