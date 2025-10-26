import redis

# Redis client
cache = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)

def cache_set(key, value, ttl=300):
    """Set a value in Redis with TTL (default 5 mins)."""
    cache.setex(key, ttl, value)

def cache_get(key):
    """Get a value from Redis."""
    return cache.get(key)

def cache_delete(key):
    """Delete a key from Redis."""
    cache.delete(key)
