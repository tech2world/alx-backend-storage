import requests
import redis
import time
from functools import wraps

# Initialize Redis connection
r = redis.Redis()

def track_count(method):
    """
    Decorator to track the number of times a URL was accessed.
    """
    @wraps(method)
    def wrapper(url):
        """
        wrapper function
        """
        count_key = f"count:{url}"
        current_count = r.get(count_key)
        if current_count:
            r.incr(count_key)
        else:
            r.set(count_key, 1)
        return method(url)
    return wrapper

def cache_expiring(expiration_time):
    """
    Decorator to cache the result of a URL with a specified expiration time.
    """
    def decorator(method):
        @wraps(method)
        def wrapper(url):
            cached_result = r.get(f"cache:{url}")
            if cached_result:
                return cached_result.decode('utf-8')
            result = method(url)
            r.setex(f"cache:{url}", expiration_time, result)
            return result
        return wrapper
    return decorator

@cache_expiring(10)
@track_count
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL using the requests module. 

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the given URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    get_page(url)
