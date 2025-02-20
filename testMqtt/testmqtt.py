import paho.mqtt.client as mqtt

# Configuración del broker MQTT
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "esp32/test12"

# Función que se ejecuta cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    print("Conectado con código resultante: " + str(rc))
    client.subscribe(mqtt_topic)  # Suscribirse al topic

# Función que se ejecuta cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el topic {msg.topic}: {msg.payload.decode()}")

# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configurar funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Iniciar el loop para recibir mensajes
client.loop_forever()