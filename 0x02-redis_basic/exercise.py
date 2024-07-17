#!/usr/bin/env python3
"""Module with statements of storing data with redis"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    def __init__(self):
        """
        Initializes an instance of the class cache.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

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
