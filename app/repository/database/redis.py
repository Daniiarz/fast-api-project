import redis.asyncio as redis

from config import settings

connection: redis.Redis = redis.Redis.from_url(url=settings.redis_url, decode_responses=True)
