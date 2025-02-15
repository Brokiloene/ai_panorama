from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app import config
from app.dependencies import lifespan
from app.exception_handlers import EXCEPTION_HANDLERS

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    f"/{config.system.STATIC_FILES_DIR}",
    StaticFiles(directory=config.system.STATIC_FILES_DIR),
    name="static",
)

for exc_cls, handler in EXCEPTION_HANDLERS:
    app.add_exception_handler(exc_cls, handler)
