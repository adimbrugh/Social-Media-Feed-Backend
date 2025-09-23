from django.core.cache import cache
from redis.exceptions import RedisError
from .errors import log_error
import json



def set_cache(key, value, timeout=60*5):
    """Store Python object in cache as JSON"""
    cache.set(key, json.dumps(value, default=str), timeout)

def get_cache(key):
    """Retrieve Python object from cache"""
    data = cache.get(key)
    if data:
        return json.loads(data)
    return None

def delete_cache(key: str) -> None:
    try:
        cache.delete(key)
    except RedisError as e:
        # avoid crashing app/tests if Redis down; log and continue
        log_error(e, context=f"delete_cache failed for {key}")
    except Exception as e:
        log_error(e, context=f"delete_cache unexpected error for {key}")
        