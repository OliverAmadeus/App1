import paho.mqtt.client as mqtt
import re
import requests
import time
from datetime import datetime
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model


# Configuración del broker MQTT
mqtt_broker = "test.mosquitto.org" #broker
mqtt_port = 1883 #puerto
mqtt_topic = "esp32/test11" #topic


contador1 = 0
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def leer_datos_desde_archivo(nombre_archivo):
    # Inicializar una lista para almacenar los datos
    data = []
    # Abrir el archivo y leer las líneas
    with open(nombre_archivo, 'r') as file:
        lines = file.readlines()
    # Procesar las líneas del archivo
    for line in lines:
        values = line.strip().split(',')
        values = [int(value) for value in values]
        data.append(values)
    # Crear el arreglo NumPy
    input_data = np.array(data)
    return input_data
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

########################################################
input_data = leer_datos_desde_archivo('RNA/archivo.txt')
input_data = np.transpose(input_data)
num_filas, num_columnas = input_data.shape
#########################################################
output_data1= leer_datos_desde_archivo('RNA/out_dat.txt')
output_data = output_data1[0]
#########################################################

model = load_model("RNA/modelo_red_neuronal.h5") 


# Función que se ejecuta cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    print("Conectado con código resultante: " + str(rc))
    client.subscribe(mqtt_topic)  # Suscribirse al topic


# Función que se ejecuta cuando se recibe un mensaje
def on_message(client, userdata, msg):

    try:
        if msg.topic == mqtt_topic:
            print(f"Mensaje recibido en el topic {msg.topic}: {msg.payload.decode()}")

            cadena_texto = msg.payload.decode()  # Convertir la cadena de bytes a una cadena de texto
            cadena_limpia = cadena_texto.strip("b'")  # Eliminar el prefijo b' de la cadena
            valores = cadena_limpia.split(",")  # Dividir la cadena en una lista de cadenas utilizando la coma como delimitador
            valores = [int(valor) for valor in valores if valor.strip()]
            print(valores)
            enteros = [int(valor) for valor in valores]  # Convertir cada cadena en la lista a un entero
            print(enteros)
            arreglo_numeros = enteros

            print(arreglo_numeros)
            
            input_value_scaled = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for i in range (16):
                input_value_scaled[i] = arreglo_numeros[i] / np.max(input_data[i])
                    #input_value_scaled = input_value / np.max(input_data)
            combined_input_value = np.array([input_value_scaled])

                    # Realizar la predicción con la red neuronal
                
            output_value_scaled = model.predict(np.array([input_value_scaled]))

                    # Desescalar el valor de salida para obtener el resultado final

            output_value = output_value_scaled * np.max(output_data)

                    # Mostrar el resultado
                    
            print("Resultado de la red neuronal para el valor de entrada ingresado:")
            with open('VALORES/Irradiancia.txt', 'w') as f:
                f.write(str(output_value[0][0]))
            print(output_value[0][0])  # Convertir el resultado a un número escalar

    except Exception as e:
            print(f"Se produjo un error: {e}")  
        

    print(msg.topic + " " + str(msg.payload))
# Crear una instancia del cliente MQTT
client = mqtt.Client()

# Configurar funciones de callback
client.on_connect = on_connect
client.on_message = on_message

# Conectar al broker MQTT
client.connect(mqtt_broker, mqtt_port, 60)

# Iniciar el loop para recibir mensajes
client.loop_forever()