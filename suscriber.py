import paho.mqtt.client as mqtt

broker = "172.18.3.235"  # IP del celular
port = 1883
topic = "test/topic"

def on_message(client, userdata, msg):
    print(f"Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

print(f"Conectando a {broker}:{port} ...")
client.connect(broker, port, 60)
client.subscribe(topic)

print(f"Suscrito a '{topic}', esperando mensajes...")
client.loop_forever()
