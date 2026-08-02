from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Production-oriented platform for autonomous enterprise AI workflows.",
)

app.include_router(health_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": "0.1.0",
    }