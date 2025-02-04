import logging.handlers
import os
from dotenv import load_dotenv

load_dotenv()

GEN_TITLE_SERVER_URL   = os.getenv("GEN_TITLE_SERVER_URL")
GEN_ARTICLE_SERVER_URL = os.getenv("GEN_ARTICLE_SERVER_URL")
GEN_IMAGE_SERVER_URL   = os.getenv("GEN_IMAGE_SERVER_URL")

STATIC_FILES_DIR  = "src/static"
TEMPLATES_DIR     = "src/templates"
IMAGES_DIR        = "src/static/images"
IMAGE_PLACEHOLDER = "src/static/images/placeholder.png"

import logging

LOG_FILE_MAX_BYTES_SIZE = 1024 * 10 # 10 kB
LOG_PATH = "logs/app.log"


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.handlers.RotatingFileHandler(
    LOG_PATH,
    maxBytes=LOG_FILE_MAX_BYTES_SIZE,
    backupCount=0
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
