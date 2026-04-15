import os
import requests
from datetime import datetime
import sys

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        print(f" Variável de ambiente obrigatória não definida: {key}")
        sys.exit(1)
    return value


class WeatherService:
    def __init__(self):
        base_url = get_env("OPEN_METEO_URL")
        lat = get_env("LAT")
        lon = get_env("LON")

        self.api_url = (
            f"{base_url}?latitude={lat}&longitude={lon}"
            "&current_weather=true"
            "&hourly=relativehumidity_2m,uv_index,precipitation_probability,apparent_temperature,cloudcover"
        )

        print("WeatherService configurado com sucesso")
        print("URL:", self.api_url)

    def fetch_weather(self):
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            cw = data["current_weather"]
            hourly = data["hourly"]

            t = datetime.fromisoformat(cw["time"])
            t_hour = t.replace(minute=0, second=0).isoformat(timespec="minutes")

            try:
                idx = hourly["time"].index(t_hour)
            except ValueError:
                idx = 0

            uv = hourly["uv_index"][idx]
            rain = hourly["precipitation_probability"][idx]
            cloud = hourly["cloudcover"][idx]

            condition = self.resolve_condition(uv, rain, cloud)

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
            print(f" Erro HTTP ao buscar clima: {e}")
            return None
        except KeyError as e:
            print(f" Erro ao acessar campo inesperado da API: {e}")
            return None
        except Exception as e:
            print(f" Erro inesperado no WeatherService: {e}")
            return None

    def resolve_condition(self, uv, precipitation, cloudcover):
        if precipitation >= 60:
            return "Chuvoso"

        if cloudcover >= 70:
            return "Nublado"

        if uv >= 6 and cloudcover < 40:
            return "Ensolarado"

        if cloudcover >= 40:
            return "Parcialmente nublado"

        return "Indefinido"
