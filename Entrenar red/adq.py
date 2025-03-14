import paho.mqtt.client as mqtt
import time
import datetime

# Configuración del broker MQTT
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "esp32/test11"

# Obtener la fecha actual para los nombres de archivo
fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
archivo_datos = f"datos_recibidos_{fecha_actual}.txt"
archivo_manual = f"datos_manual_{fecha_actual}.txt"

# Función para guardar datos en un archivo
def guardar_en_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, "a") as file:
        file.write(contenido + "\n")

# Función que se ejecuta cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado exitosamente al broker MQTT")
        client.subscribe(mqtt_topic)  # Suscribirse al topic
    else:
        print(f"Error de conexión: {rc}")

# Función que se ejecuta cuando se recibe un mensaje
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode().strip()  # Quita espacios extra
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Agrega fecha y hora
        print(f"[{timestamp}] Mensaje recibido en {msg.topic}: {data}")
        
        # Guardar datos recibidos en el archivo
        guardar_en_archivo(archivo_datos, f"{timestamp} - {data}")
        print(f"Datos guardados en {archivo_datos}")

        # Solicitar entrada manual del usuario
        entrada_manual = input("Ingrese el dato manual que desea guardar: ")
        guardar_en_archivo(archivo_manual, f"{timestamp} - {entrada_manual}")
        print(f"Dato manual guardado en {archivo_manual}")

    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# Función que maneja la desconexión y reintenta conectarse
def on_disconnect(client, userdata, rc):
    print("Desconectado del broker. Intentando reconectar...")
    while True:
        try:
            client.reconnect()
            print("Reconectado exitosamente")
            break
        except:
            print("Fallo en la reconexión, reintentando en 5 segundos...")
            time.sleep(5)

# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configurar funciones de callback
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Conectar al broker MQTT con manejo de errores
try:
    client.connect(mqtt_broker, mqtt_port, 60)
except Exception as e:
    print(f"Error al conectar con el broker: {e}")

# Iniciar el loop para recibir mensajes
client.loop_forever()
