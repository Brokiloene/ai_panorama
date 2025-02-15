import uvicorn

from app import config
from app.app import mainApp

if __name__ == "__main__":
    uvicorn.run(
        mainApp,
        host="0.0.0.0",
        port=8000,
        log_config=None,
        ssl_certfile=config.app.TLS_CERTIFICATE,
        ssl_keyfile=config.app.TLS_PRIVATE_KEY,
        ssl_ciphers="TLSv1",
    )
