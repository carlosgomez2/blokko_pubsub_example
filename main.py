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

# Carga las credenciales JSON desde el archivo y configura la audiencia.
service_account_info = json.load(open("credentials.json"))

# Configura las credenciales para el Subscriber.
subscriber_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
subscriber_credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=subscriber_audience)

# Configura las credenciales para el Publisher.
publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
publisher_credentials = jwt.Credentials.from_service_account_info(service_account_info, audience=publisher_audience)

# Configura el cliente del editor con las credenciales del Publisher.
publisher = pubsub_v1.PublisherClient(credentials=publisher_credentials)
topic_path = publisher.topic_path(project_id, topic_name)

# Configura el cliente del suscriptor con las credenciales del Subscriber.
subscriber = pubsub_v1.SubscriberClient(credentials=subscriber_credentials)
subscription_path = subscriber.subscription_path(project_id, subscription_name)


# Ruta para publicar un mensaje.


@app.route('/publish', methods=['POST'])
def publish_message():
    message_data = "Hello friend!"  # Mensaje a publicar.

    # Publica el mensaje en el tema 'blokkoMQTest'.
    pub = publisher.publish(topic_path, data=message_data.encode('utf-8'))
    pub.result()

    # Retorna un mensaje de éxito donde dice que se encoló el mensaje.
    return jsonify({'message': 'Mensaje publicado con exito', 'result': pub.result()})


# Función para manejar los mensajes recibidos.


def callback(message):
    print(f"Mensaje recibido: {message.data.decode('utf-8')}")
    message.ack()


# Ruta para iniciar la suscripción.


@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Configura los nombres de tema y suscripción.
    project_id = 'blokkodev'
    topic_name = 'blokkoMQTest'
    subscription_name = 'testQueue'

    topic_path = f'projects/{project_id}/topics/{topic_name}'
    subscription_path = f'projects/{project_id}/subscriptions/{subscription_name}'

    # Utiliza el cliente del suscriptor.
    subscriber = pubsub_v1.SubscriberClient()

    try:
        # Crea una suscripción si no existe.
        subscription = Subscription(name=subscription_path, topic=topic_path)
        subscriber.create_subscription(request=subscription)

        # Inicia la suscripción y proporciona la función de devolución de llamada.
        future = subscriber.subscribe(subscription_path, callback=callback)

        # Espera a que termine la suscripción.
        future.result()

        return jsonify({'message': 'Suscripción iniciada'})
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        subscriber.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
