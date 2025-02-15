from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import config
from .dependencies import lifespan
from .exception_handlers import EXCEPTION_HANDLERS
from .routes import main_router

mainApp = FastAPI(lifespan=lifespan)
mainApp.include_router(main_router)

mainApp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mainApp.mount(
    f"/{config.app.STATIC_FILES_DIR}",
    StaticFiles(directory=config.app.STATIC_FILES_DIR),
    name="static",
)

for exc_cls, handler in EXCEPTION_HANDLERS:
    mainApp.add_exception_handler(exc_cls, handler)
