from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

app = Flask(__name__)

# Configura las credenciales de Google Cloud Pub/Sub.
# Reemplaza 'tu-proyecto' y 'tu-credencial.json' con tus propios valores.
project_id = 'blokkodev'
topic_name = 'blokkoMQTest'
subscription_name = 'testQueue'

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_name)

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)


@app.route('/publish', methods=['POST'])
def publish_message():
    message_data = request.json.get('message')

    # Publica el mensaje en el topic_name.
    future = publisher.publish(topic_path, data=message_data.encode('utf-8'))
    future.result()

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
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(streaming_pull_future)

    return jsonify({'message': 'Suscripción iniciada'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
