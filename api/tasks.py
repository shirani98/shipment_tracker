from celery import shared_task
from django.core.cache import cache
from .utils import fetch_weather_data
import time


@shared_task
def update_weather_data():
    # Get all keys with the "zipcode_*" prefix
    keys = cache.keys("zipcode_*")

    for key in keys:
        # Extract the ZIP code from the key
        zip_code = key.split("_")[1]

        # Get weather data using the ZIP code
        new_data = fetch_weather_data(zip_code)
        if new_data is not None:
            cache.set(key, new_data)

        time.sleep(2)
