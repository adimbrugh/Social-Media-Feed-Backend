from django.core.cache import cache
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

def delete_cache(key):
    """Delete a cache key"""
    cache.delete(key)
