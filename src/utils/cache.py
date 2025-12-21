from flask_caching import Cache
from functools import wraps
from src.configs.config import Config

cache = None

def init_cache(app):
    """Initialize Flask-Caching for the Dash application.

    Sets up the global cache instance with configuration from Config. Must be
    called before using the @cached decorator.

    Args:
        app: Dash application instance with a Flask server.

    Examples:
        >>> from dash import Dash
        >>> app = Dash(__name__)
        >>> init_cache(app)
    """
    global cache
    cache = Cache(app.server, config=Config.get_cache_config())

def cached(timeout=None):
    """Decorator to cache function results using Flask-Caching.

    Wraps a function to cache its return value based on input arguments.
    Subsequent calls with the same arguments return cached results without
    re-executing the function. Uses memoization strategy.

    Args:
        timeout: Cache timeout in seconds. If None, uses Config.CACHE_TIMEOUT
            from application configuration. Default is None.

    Returns:
        Decorator function that wraps the target function with caching logic.

    Examples:
        >>> @cached(timeout=300)
        ... def expensive_computation(n):
        ...     return sum(range(n))
        >>>
        >>> # First call computes and caches
        >>> result = expensive_computation(1000000)
        >>> # Second call returns cached result
        >>> result = expensive_computation(1000000)
        >>>
        >>> # Use default timeout from config
        >>> @cached()
        ... def get_data():
        ...     return load_data_from_db()
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