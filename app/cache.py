import redis

cache = redis.Redis(
    host="localhost",   # Redis runs locally via Docker port mapping
    port=6379,
    db=0,
    decode_responses=True,
)

def cache_set(key, value, ttl=600):
    cache.setex(key, ttl, value)

def cache_get(key):
    return cache.get(key)

def cache_delete(key):
    cache.delete(key)
