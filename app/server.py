from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api import router as api_router
from app.web import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🎵 MusicMate Server started.")
    yield
    print("👋 MusicMate Server shutting down.")


app = FastAPI(
    title="MusicMate API",
    description="AI Music Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)
app.include_router(web_router)