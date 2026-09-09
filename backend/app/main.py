from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import settings
from app.api.v1.database import router as database_router
from app.api.v1.users import router as users_router
from app.api.v1.cache import router as cache_router
from app.core.logging import setup_logging

setup_logging()
#settings = settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Production-oriented platform for autonomous enterprise AI workflows.",
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(cache_router, prefix="/api/v1")
@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
    }
