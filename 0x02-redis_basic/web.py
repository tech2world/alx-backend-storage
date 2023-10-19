import requests
import redis
import time

# Initialize Redis connection
r = redis.Redis()

def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL using the requests module. 
    Tracks the number of times the URL was accessed and caches the result with an expiration time of 10 seconds.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the given URL.
    """
    # Check if the URL exists in the cache
    cached_result = r.get(f"cache:{url}")
    if cached_result:
        return cached_result.decode('utf-8')

    # Fetch the content if not present in the cache
    response = requests.get(url)
    content = response.text

    # Update the cache with the fetched content and set expiration time
    r.setex(f"cache:{url}", 10, content)

    # Update the count for the URL
    count_key = f"count:{url}"
    current_count = r.get(count_key)
    if current_count:
        r.incr(count_key)
    else:
        r.set(count_key, 1)

    return content

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https://www.google.com"
    print(get_page(url))
    time.sleep(5)  # Simulating the delay for testing expiration
    print(get_page(url))
