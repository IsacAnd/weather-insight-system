import json
import os
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

import pika

from weather_service import WeatherService


def get_env(key: str) -> str:
    value = os.getenv(key)

    if not value:
        print(f"Variável de ambiente obrigatória não definida: {key}")
        sys.exit(1)

    return value


# =====================================
# ✅ SERVIDOR HTTP MÍNIMO
# =====================================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"producer ok")

    def log_message(self, format, *args):
        pass


def start_health_server():
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health server ouvindo na porta {port}")
    server.serve_forever()


def connect_rabbitmq(parameters, queue_name: str):
    while True:
        try:
            print("Conectando ao RabbitMQ...")
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            print("Conectado ao RabbitMQ!")
            return connection, channel

        except pika.exceptions.AMQPConnectionError as e:
            print(
                f"RabbitMQ indisponível ({e}). "
                "Nova tentativa em 5 segundos..."
            )
            time.sleep(5)


# =====================================
# ✅ LOOP PRINCIPAL DO PRODUCER
# =====================================
# Toda inicialização acontece DENTRO desta função,
# que roda em thread separada — garante que o health
# server HTTP sobe primeiro e o Render detecta a porta.
def run_producer_loop():
    rabbitmq_url = get_env("RABBITMQ_URL")
    queue_name = get_env("RABBITMQ_QUEUE")
    interval = int(get_env("INTERVAL_SECONDS"))

    parameters = pika.URLParameters(rabbitmq_url)
    parameters.heartbeat = 30
    parameters.blocked_connection_timeout = 60

    weather = WeatherService()

    print(f"Intervalo de coleta: {interval} segundos")

    connection, channel = connect_rabbitmq(parameters, queue_name)

    print("Producer iniciado e publicando dados...")

    while True:
        try:
            if connection.is_closed:
                print("Conexão RabbitMQ fechada. Reconectando...")
                connection, channel = connect_rabbitmq(parameters, queue_name)

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
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                }

                json_msg = json.dumps(message)

                channel.basic_publish(
                    exchange="",
                    routing_key=queue_name,
                    body=json_msg,
                    properties=pika.BasicProperties(delivery_mode=2),
                )

                print(f"Published: {json_msg}")

        except (
            pika.exceptions.AMQPConnectionError,
            pika.exceptions.StreamLostError,
            pika.exceptions.ChannelWrongStateError,
            pika.exceptions.ConnectionClosed,
        ) as e:
            print(f"Conexão com RabbitMQ perdida: {e}")
            print("Tentando reconectar...")
            connection, channel = connect_rabbitmq(parameters, queue_name)

        except Exception as e:
            print(f"Erro ao publicar mensagem: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    # Loop de coleta roda em thread daemon separada.
    # A thread principal serve o health check HTTP —
    # o Render detecta a porta e considera o serviço ativo.
    producer_thread = threading.Thread(target=run_producer_loop, daemon=True)
    producer_thread.start()

    # Bloqueia na thread principal servindo o health check
    start_health_server()