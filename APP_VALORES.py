import paho.mqtt.client as mqtt

# Configuración del broker MQTT
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883
mqtt_topic = "esp32/test12"

def mapear_valor(valor, entrada_min, entrada_max, salida_min, salida_max):
    return salida_min + (valor - entrada_min) * (salida_max - salida_min) / (entrada_max - entrada_min)

# Función que se ejecuta cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    print("Conectado con código resultante: " + str(rc))
    client.subscribe(mqtt_topic)  # Suscribirse al topic

# Función que se ejecuta cuando se recibe un mensaje
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el topic {msg.topic}: {msg.payload.decode()}")

    cadena_texto1 = msg.payload.decode()  # Convertir la cadena de bytes a una cadena de texto
    cadena_limpia1 = cadena_texto1.strip("b'")  # Eliminar el prefijo b' de la cadena
    valores1 = cadena_limpia1.split(",")  # Dividir la cadena en una lista de cadenas utilizando la coma como delimitador
    enteros1 = [float(valor1) for valor1 in valores1]  # Convertir cada cadena en la lista a un entero
    print(enteros1)
    with open('VALORES/VoltajeIN.txt', 'w') as f:
        f.write(str(int(mapear_valor(enteros1[2], 0, 4095, 0, 97))))

    with open('VALORES/CorrienteIN.txt', 'w') as f:
        f.write(str(enteros1[5]))

    potenciaIN = round(float((enteros1[5]* int(mapear_valor(enteros1[2], 0, 4095, 0, 97)))),2)
    with open('VALORES/PotenciaIN.txt', 'w') as f:
        f.write(str(potenciaIN))
    voltajeout  = round(  (float(mapear_valor(enteros1[0], 0, 4095, 0, 97))), 2)
    print(voltajeout)
    if voltajeout > 12 and voltajeout < 13:
        with open('VALORES/VoltajeOUT.txt', 'w') as f:
                f.write(str(float(voltajeout)))
    corrienteOUT = round(float((potenciaIN * .65) / 12),2)  
    with open('VALORES/CorrienteOUT.txt', 'w') as f:
        f.write(str(corrienteOUT))
    potenciaOUT = round(float(potenciaIN * .65),2)
    with open('VALORES/PotenciaOUT.txt', 'w') as f:
        f.write(str(potenciaOUT))                      

    with open('VALORES/Ciclodetrabajo.txt', 'w') as f:
        f.write(str(int((12 * 100)/  int(mapear_valor(enteros1[2], 0, 4095, 0, 97)))))



# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configurar funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Iniciar el loop para recibir mensajes
client.loop_forever()