from fastapi import APIRouter

from .ai_gen import router as ai_gen_router
from .articles import router as articles_router
from .root import router as root_router

router = APIRouter()
router.include_router(root_router)
router.include_router(articles_router)
router.include_router(ai_gen_router)
