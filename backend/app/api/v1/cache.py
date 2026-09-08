from fastapi import APIRouter
from app.cache.redis_client import get_redis

router = APIRouter(tags=["Cache"])


@router.post("/cache")
def set_cache():
    r = get_redis()
    r.set("test_key", "hello_redis")

    return {"status": "value_set"}


@router.get("/cache")
def get_cache():
    r = get_redis()
    value = r.get("test_key")

    return {"value": value}