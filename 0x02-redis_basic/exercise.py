#!/usr/bin/env python3
"""
Create a Cache class. In the __init__ method, store an instance of the Redis
client as a private variable named _redis (using redis.Redis()) and flush
the instance using flushdb.

"""


import redis
import uuid
from typing import Callable, Union
from functools import wraps


def count_calls(fn: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        fn (Callable): The method to be counted.

    Returns:
        Callable: The wrapped method with call count functionality.
    """
    key = fn.__qualname__

    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return fn(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a function.

    Args:
        method (Callable): The method for which the history needs to be stored

    Returns:
        Callable: The wrapped method with history storage functionality.
    """
    inputs_key = "{}:inputs".format(method.__qualname__)
    outputs_key = "{}:outputs".format(method.__qualname__)

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, str(output))
        return output

    return wrapper


def replay(self, method: Callable):
    """
    Displays the history of calls of a particular function.

    Args:
        method (Callable): The method for which the history
        of calls is to be displayed.
    """
    inputs_key = "{}:inputs".format(method.__qualname__)
    outputs_key = "{}:outputs".format(method.__qualname__)

    inputs = self._redis.lrange(inputs_key, 0, -1)
    outputs = self._redis.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for args, output in zip(inputs, outputs):
        print(
            f"{method.__qualname__}{args.decode('utf-8')} -> \
                    {output.decode('utf-8')}")


class Cache:
    """
    A class representing a simple cache utilizing Redis.
    """

    def __init__(self):
        """
        Initializes a Redis client and flushes the instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis under a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]):
            The data to be stored in the cache.

        Returns:
            str: The randomly generated key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """
        Retrieves the data from Redis under the given key and applies
        the optional conversion function.

        Args:
            key (str): The key to retrieve the data from Redis.
            fn (Callable, optional): The function used to convert
            the data back to the desired format.

        Returns:
            Union[str, bytes, int, None]: The retrieved data from Redis after
              applying the conversion function if provided.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, None]:
        """
        Retrieves the data from Redis under the given key as a string.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
            Union[str, bytes, None]: The retrieved data from Redis as a string
        """
        return self.get(key, fn=lambda d: d.decode(
            "utf-8") if isinstance(d, bytes) else d)

    def get_int(self, key: str) -> Union[int, bytes, None]:
        """
        Retrieves the data from Redis under the given key as an integer.

        Args:
            key (str): The key to retrieve the data from Redis.

        Returns:
          Union[int, bytes, None]:The retrieved data from Redis as an integer
        """
        return self.get(key, fn=lambda d: int(d) if isinstance(d,
                                                               bytes) else d)
