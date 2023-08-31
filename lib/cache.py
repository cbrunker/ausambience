from datetime import datetime

import orjson
import redis.asyncio as redis
from config import settings


connection_pool = redis.Redis.from_url(settings.REDIS_URL, password=settings.REDIS_SECRET)


def get_redis_conn() -> redis.ConnectionPool:
    """
    Returns the async Redis client instance.
    """
    return connection_pool


async def cache_in_redis(key: str, value: dict, ttl: int = settings.REDIS_TTL):
    """
    Asynchronously cache a dictionary in Redis with a specified time-to-live (TTL).

    The function enhances the value dictionary with a 'cached_time' key, providing the timestamp at which the
    data was cached. This timestamp uses the ISO 8601 format.

    :param key: Redis storage key value
    :param value: dict data to be cached
    :param ttl: The time-to-live duration in seconds. This defines how long the data remains in the cache
                before it expires

    :raises: Any exception raised by the Redis client during the caching operation
    """
    # redis does not store key creation time, create timestamp and inject into value dictionary as metadata
    conn = get_redis_conn()
    value['cached_time'] = datetime.utcnow().isoformat()

    await conn.setex(key, ttl, orjson.dumps(value))


async def fetch_from_redis(key: str) -> dict | None:
    """
    Fetch a dictionary from Redis

    :param key: Redis key
    :return: Data from Redis or None if not found
    """
    conn = get_redis_conn()
    cached_value = await conn.get(key)

    if cached_value:
        return orjson.loads(cached_value)
