from flask_caching import Cache
from functools import wraps
from config import Config

cache = None

def init_cache(app):
    global cache
    cache = Cache(app.server, config=Config.get_cache_config())

def cached(timeout=None):
    """
    Decorator to cache function results using Flask-Caching.

    Args:
        timeout: Cache timeout in seconds. If None, uses Config.CACHE_TIMEOUT

    Returns:
        Decorator function that wraps the target function with caching
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache is not None:
                cache_timeout = timeout if timeout is not None else Config.CACHE_TIMEOUT
                return cache.memoize(cache_timeout)(func)(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator