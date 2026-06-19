import os
import sys
from datetime import datetime

import requests


def get_env(key: str) -> str:
    value = os.getenv(key)

    if not value:
        print(
            f"Variável de ambiente obrigatória não definida: {key}"
        )
        sys.exit(1)

    return value


# Fortaleza como fallback caso o backend não responda
DEFAULT_LAT = -3.7172
DEFAULT_LON = -38.5433


class WeatherService:
    def __init__(self):
        self.base_url = get_env("OPEN_METEO_URL")
        self.backend_url = get_env("BACKEND_INTERNAL_URL")
        self.session = requests.Session()

        print("WeatherService configurado com sucesso")

    def fetch_coords(self) -> tuple[float, float]:
        """
        Busca as coordenadas salvas no backend.
        Retorna Fortaleza como fallback se o backend não responder
        ou ainda não tiver coords salvas.
        """
        try:
            response = self.session.get(
                f"{self.backend_url}/api/location",
                timeout=5,
            )

            response.raise_for_status()

            data = response.json()

            lat = data["latitude"]
            lon = data["longitude"]

            print(f"Coordenadas obtidas do backend: lat={lat}, lon={lon}")

            return lat, lon

        except Exception as e:
            print(
                f"Erro ao buscar coordenadas do backend ({e}). "
                f"Usando fallback: lat={DEFAULT_LAT}, lon={DEFAULT_LON}"
            )

            return DEFAULT_LAT, DEFAULT_LON

    def build_api_url(self, lat: float, lon: float) -> str:
        return (
            f"{self.base_url}?latitude={lat}&longitude={lon}"
            "&current_weather=true"
            "&hourly=relativehumidity_2m,"
            "uv_index,"
            "precipitation_probability,"
            "apparent_temperature,"
            "cloudcover"
        )

    def fetch_weather(self):
        lat, lon = self.fetch_coords()

        api_url = self.build_api_url(lat, lon)

        try:
            response = self.session.get(
                api_url,
                timeout=10,
            )

            response.raise_for_status()

            data = response.json()

            cw = data["current_weather"]
            hourly = data["hourly"]

            t = datetime.fromisoformat(cw["time"])

            t_hour = t.replace(
                minute=0,
                second=0,
            ).isoformat(timespec="minutes")

            try:
                idx = hourly["time"].index(t_hour)

            except ValueError:
                idx = 0

            uv = hourly["uv_index"][idx]
            rain = hourly["precipitation_probability"][idx]
            cloud = hourly["cloudcover"][idx]

            condition = self.resolve_condition(
                uv,
                rain,
                cloud,
            )

            return {
                "temperature": cw["temperature"],
                "windspeed": cw["windspeed"],
                "humidity": hourly["relativehumidity_2m"][idx],
                "uvIndex": uv,
                "precipitationChance": rain,
                "heatIndex": hourly["apparent_temperature"][idx],
                "condition": condition,
                "timestamp": cw["time"],
            }

        except requests.exceptions.RequestException as e:
            print(f"Erro HTTP ao buscar clima: {e}")
            return None

        except KeyError as e:
            print(
                f"Erro ao acessar campo inesperado da API: {e}"
            )
            return None

        except Exception as e:
            print(
                f"Erro inesperado no WeatherService: {e}"
            )
            return None

    def resolve_condition(
        self,
        uv,
        precipitation,
        cloudcover,
    ):
        if precipitation >= 60:
            return "Chuvoso"

        if cloudcover >= 70:
            return "Nublado"

        if uv >= 6 and cloudcover < 40:
            return "Ensolarado"

        if cloudcover >= 40:
            return "Parcialmente nublado"
        
        if cloudcover < 40:
            return "Céu limpo"

        return "Indefinido"