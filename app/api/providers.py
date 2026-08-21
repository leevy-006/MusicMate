from fastapi import APIRouter
from config.settings import LLM_CONFIGS

router = APIRouter(tags=["providers"])

@router.get("/providers")
async def list_providers():
    return {"providers": list(LLM_CONFIGS.keys())}