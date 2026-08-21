from fastapi import APIRouter
from app.web import pages

router = APIRouter()
router.include_router(pages.router)