from fastapi import APIRouter
from app.api import chat, providers

router = APIRouter(prefix="/api")

router.include_router(chat.router)
router.include_router(providers.router)