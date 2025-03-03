import logging
import logging.handlers
import sys

from dotenv import load_dotenv

load_dotenv()

STATIC_FILES_DIR = "static"

TEMPLATES_DIR = "src/templates"

TLS_CERTS_DIR = "certs"
TLS_CERTIFICATE = "certs/public.crt"
TLS_PRIVATE_KEY = "certs/private.key"
TLS_COMBINED_CERT = "certs/combined.pem"

IMAGE_PLACEHOLDER = "static/images/placeholder.png"


LOG_FILE_MAX_BYTES_SIZE = 1024 * 10  # 10 kB
LOG_PATH = "logs/app.log"


logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.handlers.RotatingFileHandler(
    LOG_PATH, maxBytes=LOG_FILE_MAX_BYTES_SIZE, backupCount=0
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(logging.StreamHandler(sys.stdout))
