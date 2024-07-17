import redis
import uuid
from typing import Union

class Cache:
    def __init__(self):
        """
        Initializes an instance of the class.
        """
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
            """
            Stores the given data in Redis and returns the generated key.

            Args:
                data (Union[str, bytes, int, float]): The data to be stored in Redis.

            Returns:
                str: The generated key used to store the data in Redis.
            """
            key = str(uuid.uuid4())
            self._redis.set(key, data)
            return key
