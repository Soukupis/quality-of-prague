import pandas as pd
from flask_caching import Cache
from functools import wraps

cache = None

def init_cache(app):
    global cache
    cache = Cache(app.server, config={'CACHE_TYPE': 'SimpleCache'})

def cached(timeout=300):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache is not None:
                return cache.memoize(timeout)(func)(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@cached(timeout=300)
def get_data1():
    # load dataset 1
    return []

@cached(timeout=300)
def get_data2():
    # load dataset 2
    return []