from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.api.v1.database import router as database_router
from app.database.init_db import init_db
from app.api.v1.users import router as users_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Production-oriented platform for autonomous enterprise AI workflows.",
)

app.include_router(health_router, prefix="/api/v1")
app.include_router(database_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": "0.1.0",
    }

@app.on_event("startup")
def on_startup():
    init_db()