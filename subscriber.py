# Description: Código de ejemplo para publicar y suscribirse a un tema de Google Cloud Pub/Sub.
# Doc: https://pypi.org/project/google-cloud-pubsub/
# Credentials: https://console.cloud.google.com/apis/credentials?authuser=1&project=blokkodev

import os
import json


from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import Subscription
from google.auth import jwt

app = Flask(__name__)


# Configura las credenciales de Google Cloud Pub/Sub.
# Reemplaza con la ruta real de tus credenciales.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

project_id = 'blokkodev'
topic_name = 'blokkoMQTest'
subscription_name = 'testQueue'

topic_path = f'projects/{project_id}/topics/{topic_name}'
subscription_path = f'projects/{project_id}/subscriptions/{subscription_name}'

# Carga las credenciales JSON desde el archivo y configura la audiencia.
service_account_info = json.load(open("credentials.json"))

# Configura las credenciales para el Subscriber.
subscriber_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
subscriber_credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=subscriber_audience)


# Configura el cliente del suscriptor con las credenciales del Subscriber.
subscriber = pubsub_v1.SubscriberClient(credentials=subscriber_credentials)
subscription_path = subscriber.subscription_path(project_id, subscription_name)


# Función para manejar los mensajes recibidos.
def callback(message):
    print(f"Mensaje recibido: {message.data.decode('utf-8')}")
    message.ack()


# Utiliza el cliente del suscriptor.
def start_subscription():
    print("Iniciando suscripcion...")
    try:
        # Inicia la suscripción y proporciona la función de devolución de llamada.
        future = subscriber.subscribe(subscription_path, callback=callback)

        # Espera a que termine la suscripción.
        future.result()

        return jsonify({'message': 'Suscripción iniciada'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        subscriber.close()


# Llama a la función para iniciar la suscripción cuando se inicia la aplicación.
start_subscription()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)
