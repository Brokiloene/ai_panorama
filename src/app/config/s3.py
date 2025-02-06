import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY    = os.getenv("S3_ACCESS_KEY")
SECRET_KEY    = os.getenv("S3_SECRET_KEY")
ADDR          = os.getenv("S3_ADDR")
PORT          = os.getenv("S3_PORT")
URL           = f"http://{ADDR}:{PORT}"
NEWS_IMGS_BUCKET = os.getenv("NEWS_IMGS_BUCKET")
