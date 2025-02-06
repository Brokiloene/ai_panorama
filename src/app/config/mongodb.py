import os
from dotenv import load_dotenv
load_dotenv()

USER = os.getenv("MONGODB_USER")
PASS = os.getenv("MONGODB_PASS")
ADDR = os.getenv("MONGODB_ADDR")
PORT = os.getenv("MONGODB_PORT")

URL = f"mongodb://{USER}:{PASS}@{ADDR}:{PORT}/?tls=true"

import app.config as config

client_config = {
    "host": URL,
    "tls": True,
    "tlsCertificateKeyFile": config.system.TLS_COMBINED_CERT,
    "tlsAllowInvalidCertificates": True
}