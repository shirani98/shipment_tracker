from django.test import TestCase
from .models import Shipment
from unittest.mock import Mock, patch
from .utils import (
    get_weather_data,
    set_popular_zipcode_to_cache,
    POPULAR_ZIPCODES,
    fetch_weather_data,
)
from django.core.cache import cache


class ShipmentModelTest(TestCase):
    def test_extract_city_from_address_with_zipcode(self):
        shipment = Shipment()
        zip_code = shipment.extract_city_from_address("Street 10, 75001 Paris, France")
        self.assertEqual(zip_code, "75001")

    def test_extract_city_from_address_without_zipcode(self):
        shipment = Shipment()
        zip_code = shipment.extract_city_from_address("Street 10, Paris, France")
        self.assertIsNone(zip_code)

    def test_extract_city_from_address_with_invalid_zipcode(self):
        shipment = Shipment(
            tracking_number="TN12345678",
            carrier="DHL",
            sender_address="Street 1, 10115 Berlin, Germany",
            receiver_address="Street 10, invalid Paris, France",
            article_name="Laptop",
            article_quantity=1,
            article_price=800,
            SKU="LP123",
            status="in-transit",
        )
        shipment.save()
        self.assertEqual(shipment.receiver_zip_code, None)


class FetchWeatherDataTest(TestCase):
    @patch("api.utils.requests.get")
    def test_fetch_weather_data_success(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"temp": 25}]}
        mock_requests_get.return_value = mock_response

        zip_code = "75001"
        result = fetch_weather_data(zip_code)

        self.assertEqual(result, 25)

    @patch("api.utils.requests.get")
    def test_fetch_weather_data_failure(self, mock_requests_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        zip_code = "75001"
        result = fetch_weather_data(zip_code)

        self.assertIsNone(result)

    @patch("api.utils.requests.get")
    def test_fetch_weather_data_exception(self, mock_requests_get):
        mock_requests_get.side_effect = Exception("API error")

        zip_code = "75001"
        result = fetch_weather_data(zip_code)

        self.assertIsNone(result)


class SetPopularZipcodeToCacheTest(TestCase):
    def test_set_popular_zipcode_to_cache(self):
        cache.clear()
        set_popular_zipcode_to_cache()
        self.assertEqual(len(POPULAR_ZIPCODES), len(cache.keys("zipcode_*")))


class GetWeatherDataTest(TestCase):
    @patch("api.utils.cache.get")
    @patch("api.utils.fetch_weather_data")
    def test_get_weather_data_from_cache(self, mock_fetch_weather_data, mock_cache_get):
        zip_code = "75001"
        cached_data = 25
        mock_cache_get.return_value = cached_data

        result = get_weather_data(zip_code)

        self.assertEqual(result, cached_data)

        mock_fetch_weather_data.assert_not_called()

    @patch("api.utils.cache.get")
    @patch("api.utils.fetch_weather_data")
    def test_get_weather_data_not_in_cache(
        self, mock_fetch_weather_data, mock_cache_get
    ):
        zip_code = "75001"
        mock_cache_get.return_value = None

        mock_fetch_weather_data.return_value = 25

        result = get_weather_data(zip_code)

        self.assertEqual(result, 25)

        mock_cache_get.assert_called_once_with(f"zipcode_{zip_code}")
        mock_fetch_weather_data.assert_called_once_with(zip_code)
