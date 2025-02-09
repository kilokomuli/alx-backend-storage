#!/usr/bin/env python3
"""A module with tools for request caching and tracking."""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """Caches the output of fetched data."""
    @wraps(method)
    def invoker(url):
        """The wrapper function for caching the output."""
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'cached:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.setex(f'cahed:{url}', 10, result)
        return result
    return invoker


@cache_page
def get_page(url: str) -> str:
    """Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    re = requests.get(url)
    return re.text
