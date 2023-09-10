from django.core.cache import cache
import requests
from django.conf import settings

POPULAR_ZIPCODES = [
    "20001",
    "75001",
    "10115",
    "00184",
    "28001",
    "04522",
    "11511",
    "00100",
    "11564",
    "06000",
]


def get_weather_data(zip_code):
    # Attempt to retrieve weather data from cache
    zipcode_key = f"zipcode_{zip_code}"
    cached_data = cache.get(zipcode_key)

    if cached_data is not None:
        return cached_data

    # If not in cache or cache has expired, fetch and set new data
    new_data = fetch_weather_data(zip_code)
    if new_data is not None:
        # Set a cache timeout, e.g., cache for 2 hours
        cache.set(zipcode_key, new_data, 7200)
    return new_data


def fetch_weather_data(zip_code):
    try:
        api_url = f"https://api.weatherbit.io/v2.0/current?key={settings.WEATHER_API_KEY}&postal_code={zip_code}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()["data"][0]["temp"]
            return data
    except Exception as e:
        pass

    return None


def set_popular_zipcode_to_cache():
    for zip_code in POPULAR_ZIPCODES:
        cache_key = f"zipcode_{zip_code}"
        if not cache.get(cache_key):
            cache.set(cache_key, None)
