import os
import pdb

from flask import Flask, request, jsonify
from google.cloud import pubsub_v1  # Importa la librería de Google Cloud Pub/Sub.

app = Flask(__name__)

# Configura las credenciales de Google Cloud Pub/Sub.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"  # Reemplaza con la ruta real de tus credenciales.
project_id = 'blokkodev'  # blokkodev es el ID del proyecto de Google Cloud.
topic_name = 'blokkoMQTest'  # Nombre del tema.
subscription_name = 'testQueue'  # Nombre de la suscripción.

publisher = pubsub_v1.PublisherClient()  # Crea un cliente de publicación.
topic_path = publisher.topic_path(project_id, topic_name)  # Crea la ruta del tema.

subscriber = pubsub_v1.SubscriberClient()  # Crea un cliente de suscripción.
subscription_path = subscriber.subscription_path(project_id, subscription_name)  # Crea la ruta de la suscripción.

# Ruta para publicar un mensaje.


@app.route('/publish', methods=['POST'])
def publish_message():
    # message_data = request.json.get('message')
    message_data = "Hello friend!"  # Mensaje a publicar.

    # Publica el mensaje en el tema 'blokkoMQTest'.
    pub = publisher.publish(topic_path, data=message_data.encode('utf-8'))
    # pdb.set_trace() # Para debuggear en la consola
    pub.result()

    # Retorna un mensaje de éxito donde dice que se encolo el mensaje.
    return jsonify({'message': 'Mensaje publicado con éxito'})


# Función para manejar los mensajes recibidos.


def callback(message):
    print(f"Mensaje recibido: {message.data.decode('utf-8')}")
    message.ack()


# Ruta para iniciar la suscripción.


@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Crea una suscripción si no existe.
    subscriber.create_subscription(subscription_path)

    # Inicia la suscripción.
    streaming_pull_pub = subscriber.subscribe(subscription_path, callback=callback)
    # pdb.set_trace() # Para debuggear en la consola
    print(streaming_pull_pub)

    return jsonify({'message': 'Suscripción iniciada'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
