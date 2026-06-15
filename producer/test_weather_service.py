import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from datetime import datetime

# Define required environment variables for WeatherService initialization
os.environ["OPEN_METEO_URL"] = "https://api.open-meteo.com/v1/forecast"
os.environ["LAT"] = "-3.71722"
os.environ["LON"] = "-38.5434"

from weather_service import WeatherService


class TestWeatherService(unittest.TestCase):
    def setUp(self):
        self.service = WeatherService()

    def test_resolve_condition_chuvoso(self):
        # precipitation >= 60 -> "Chuvoso"
        self.assertEqual(self.service.resolve_condition(0, 60, 0), "Chuvoso")
        self.assertEqual(self.service.resolve_condition(10, 80, 50), "Chuvoso")

    def test_resolve_condition_nublado(self):
        # cloudcover >= 70 e precipitation < 60 -> "Nublado"
        self.assertEqual(self.service.resolve_condition(0, 0, 70), "Nublado")
        self.assertEqual(self.service.resolve_condition(5, 59, 80), "Nublado")

    def test_resolve_condition_ensolarado(self):
        # uv >= 6, cloudcover < 40 e precipitation < 60 -> "Ensolarado"
        self.assertEqual(self.service.resolve_condition(6, 0, 39), "Ensolarado")
        self.assertEqual(self.service.resolve_condition(10, 30, 10), "Ensolarado")

    def test_resolve_condition_parcialmente_nublado(self):
        # cloudcover >= 40 e < 70, e precipitation < 60 -> "Parcialmente nublado"
        self.assertEqual(self.service.resolve_condition(5, 10, 40), "Parcialmente nublado")
        self.assertEqual(self.service.resolve_condition(2, 50, 69), "Parcialmente nublado")

    def test_resolve_condition_indefinido(self):
        # outros casos
        self.assertEqual(self.service.resolve_condition(2, 10, 10), "Indefinido")

    @patch('requests.Session.get')
    def test_fetch_weather_success(self, mock_get):
        # Mocking a successful response from Open-Meteo API
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        mock_response.json.return_value = {
            "current_weather": {
                "time": "2026-06-12T15:30",
                "temperature": 25.5,
                "windspeed": 12.0
            },
            "hourly": {
                "time": ["2026-06-12T15:00", "2026-06-12T16:00"],
                "relativehumidity_2m": [80, 85],
                "uv_index": [5.0, 7.0],
                "precipitation_probability": [20, 75],
                "apparent_temperature": [26.0, 27.5],
                "cloudcover": [50, 90]
            }
        }
        mock_get.return_value = mock_response

        data = self.service.fetch_weather()
        
        self.assertIsNotNone(data)
        self.assertEqual(data["temperature"], 25.5)
        self.assertEqual(data["windspeed"], 12.0)
        self.assertEqual(data["humidity"], 80)
        self.assertEqual(data["uvIndex"], 5.0)
        self.assertEqual(data["precipitationChance"], 20)
        self.assertEqual(data["heatIndex"], 26.0)
        self.assertEqual(data["condition"], "Parcialmente nublado")
        self.assertEqual(data["timestamp"], "2026-06-12T15:30")

    @patch('requests.Session.get')
    def test_fetch_weather_http_error(self, mock_get):
        # Mocking an HTTP error (raises exception)
        import requests
        mock_get.side_effect = requests.exceptions.HTTPError("API offline")
        
        data = self.service.fetch_weather()
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
