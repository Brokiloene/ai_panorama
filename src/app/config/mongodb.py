# MONGODB_URL = "mongodb://127.0.0.1:27017"
# MONGODB_USER = "root"
# MONGODB_PASS = "rootpassword"
# MONGODB_ADDR = "172.17.0.1"
# MONGODB_PORT = "27017"

import os
from dotenv import load_dotenv
load_dotenv()

MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASS = os.getenv("MONGODB_PASS")
MONGODB_ADDR = os.getenv("MONGODB_ADDR")
MONGODB_PORT = os.getenv("MONGODB_PORT")


MONGODB_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_ADDR}:{MONGODB_PORT}"
# MONGODB_URL = "mongodb://172.17.0.1:27017"
print("================================", MONGODB_URL)
