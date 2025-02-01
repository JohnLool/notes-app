from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi import Request
from app.config import settings


def custom_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    *args,
    **kwargs,
):
    owner = request.query_params.get("owner", "all")
    user_id = request.headers.get("X-User-ID", "anonymous")
    return f"{namespace}:{request.method}:{request.url.path}:{owner}:{user_id}"


async def init_cache():
    redis = aioredis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.CACHE_PREFIX,
        key_builder=custom_key_builder
    )
