#!/usr/bin/env python3
"""Module with statements of storing data with redis"""
import redis
import uuid
from functools import wraps
from typing import Any, Union, Callable


def count_calls(method: Callable) -> Callable:
    """Implements a system to count how many times methods
    of the cache class are called
    Args:
        method (callable): The method to decorate
    Returns:
        Callable the wrapped method with counting functionality
    """
    @wraps(method)
    def counter(self: Any, *args, **kwargs) -> str:
        """Increments the count for the method call and
        then calls the method"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return counter


def call_history(method: Callable) -> Callable:
    """ Decorator for Cache class method to track args
    """
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        """ Wraps called method and tracks its passed argument by storing
            them to redis
        """
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """ Check redis for how many times a function was called and display:
    """
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    def __init__(self):
        """
        Initializes an instance of the class cache.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in Redis and returns the generated key.
        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in Redis.
        Returns:
            str: The generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """
        Retrieves the data stored in Redis under the given key.

        Args:
            key (str): The key used to store the data in Redis.
            fn (Callable): A function to be applied to the data

        Returns:
            Union[str, bytes, int, float]: The data stored in Redis
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        Retrieves the data stored in Redis under the given key as a string.

        Args:
            key (str): The key used to store the data in Redis.

        Returns:
            str: The data stored in Redis under the given key as a string.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves the data stored in Redis under the given key as an integer.

        Args:
            key (str): The key used to store the data in Redis.

        Returns:
            int: The data stored in Redis under the given key as an integer.
        """
        return self.get(key, lambda x: int(x))
