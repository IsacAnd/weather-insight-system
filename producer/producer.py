import pika
import json
import time
import os
from datetime import datetime, timezone
from weather_service import WeatherService
import sys

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        print(f"Variável de ambiente obrigatória não definida: {key}")
        sys.exit(1)
    return value


RABBITMQ_URL = get_env("RABBITMQ_URL")
RABBITMQ_QUEUE = get_env("RABBITMQ_QUEUE")
INTERVAL_SECONDS = int(get_env("INTERVAL_SECONDS"))

print("Intervalo de coleta:", INTERVAL_SECONDS, "segundos")

parameters = pika.URLParameters(RABBITMQ_URL)
weather = WeatherService()

# Tentativas de conexão com RabbitMQ
for i in range(10):
    try:
        connection = pika.BlockingConnection(parameters)
        print("Conectado ao RabbitMQ!")
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"RabbitMQ não disponível, tentando novamente em 3s... ({i+1}/10)")
        time.sleep(3)
else:
    print("Falha ao conectar no RabbitMQ")
    sys.exit(1)

channel = connection.channel()
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

print("Producer iniciado e publicando dados...")

while True:
    try:
        data = weather.fetch_weather()

        if data:
            message = {
                "temperature": data["temperature"],
                "windspeed": data["windspeed"],
                "humidity": data["humidity"],
                "uvIndex": data["uvIndex"],
                "precipitationChance": data["precipitationChance"],
                "heatIndex": data["heatIndex"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "obs_timestamp": data.get("timestamp"),
                "source": "weather-api",
                "condition": data["condition"],
            }

            json_msg = json.dumps(message)

            channel.basic_publish(
                exchange="",
                routing_key=RABBITMQ_QUEUE,
                body=json_msg,
                properties=pika.BasicProperties(delivery_mode=2)
            )

            print("Published:", json_msg)

    except Exception as e:
        print(f"Erro ao publicar mensagem: {e}")

    time.sleep(INTERVAL_SECONDS)
