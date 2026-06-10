import json
import os
import sys
import time
from datetime import datetime, timezone

import pika

from weather_service import WeatherService


def get_env(key: str) -> str:
    value = os.getenv(key)

    if not value:
        print(f"Variável de ambiente obrigatória não definida: {key}")
        sys.exit(1)

    return value


RABBITMQ_URL = get_env("RABBITMQ_URL")
RABBITMQ_QUEUE = get_env("RABBITMQ_QUEUE")
INTERVAL_SECONDS = int(get_env("INTERVAL_SECONDS"))

print(f"Intervalo de coleta: {INTERVAL_SECONDS} segundos")

parameters = pika.URLParameters(RABBITMQ_URL)

# Detecta conexões mortas mais rapidamente
parameters.heartbeat = 30
parameters.blocked_connection_timeout = 60

weather = WeatherService()


def connect_rabbitmq():
    while True:
        try:
            print("Conectando ao RabbitMQ...")

            connection = pika.BlockingConnection(parameters)

            channel = connection.channel()

            channel.queue_declare(
                queue=RABBITMQ_QUEUE,
                durable=True,
            )

            print("Conectado ao RabbitMQ!")

            return connection, channel

        except pika.exceptions.AMQPConnectionError as e:
            print(
                f"RabbitMQ indisponível ({e}). "
                "Nova tentativa em 5 segundos..."
            )

            time.sleep(5)


connection, channel = connect_rabbitmq()

print("Producer iniciado e publicando dados...")


while True:
    try:
        # Reconecta caso a conexão tenha sido encerrada
        if connection.is_closed:
            print("Conexão RabbitMQ fechada. Reconectando...")
            connection, channel = connect_rabbitmq()

        data = weather.fetch_weather()

        if data:
            message = {
                "temperature": data["temperature"],
                "windspeed": data["windspeed"],
                "humidity": data["humidity"],
                "uvIndex": data["uvIndex"],
                "precipitationChance": data["precipitationChance"],
                "heatIndex": data["heatIndex"],
                "timestamp": datetime.now(
                    timezone.utc
                ).isoformat(),
                "obs_timestamp": data.get("timestamp"),
                "source": "weather-api",
                "condition": data["condition"],
            }

            json_msg = json.dumps(message)

            channel.basic_publish(
                exchange="",
                routing_key=RABBITMQ_QUEUE,
                body=json_msg,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )

            print(f"Published: {json_msg}")

    except (
        pika.exceptions.AMQPConnectionError,
        pika.exceptions.StreamLostError,
        pika.exceptions.ChannelWrongStateError,
        pika.exceptions.ConnectionClosed,
    ) as e:

        print(
            f"Conexão com RabbitMQ perdida: {e}"
        )

        print("Tentando reconectar...")

        connection, channel = connect_rabbitmq()

    except Exception as e:
        print(f"Erro ao publicar mensagem: {e}")

    time.sleep(INTERVAL_SECONDS)