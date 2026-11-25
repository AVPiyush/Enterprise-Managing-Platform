
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.v1.database import router as database_router
from app.api.v1.users import router as users_router
from app.api.v1.cache import router as cache_router
from app.api.v1.documents import router as documents_router
from app.api.v1.indexing import router as indexing_router
from app.api.v1.search import router as search_router
from app.api.v1.chat import router as chat_router

from app.core.config import settings
from app.core.logging import setup_logging
from app.database.init_db import init_db


setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Enterprise Agent Platform for autonomous enterprise AI workflows.",
    lifespan=lifespan,
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(cache_router, prefix="/api/v1")
app.include_router(documents_router, prefix="/api/v1")
app.include_router(indexing_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
    }
