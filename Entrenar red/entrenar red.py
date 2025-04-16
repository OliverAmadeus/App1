import numpy as np
import tensorflow as tf
from tensorflow import keras

# Datos de entrada y salida
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


input_data_scaled = ([[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]])
                     
for i in range (16):
    input_data_scaled[i] =input_data[i] / np.max(input_data[i])
    
output_data_scaled = output_data / np.max(output_data)

combined_input_data = np.column_stack(input_data_scaled)

# Construir la red neuronal
model = keras.Sequential([
    keras.layers.Dense(64, activation='relu', input_shape=(16,)),  # Cambia la forma de entrada a (16,)
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1)
])

# Compilar el modelo
model.compile(optimizer='adam', loss='mse')

# Entrenar el modelo
model.fit(combined_input_data, output_data_scaled, epochs=5000, verbose=0)
valuerr = []
model.save("modelo_entrenado.h5")

# Solicitar al usuario que ingrese un valor de entrada por teclado
for h in range (1):
    for b in range (1):
       

          for k in range (len(output_data)): # 58
              
              input_value = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
              
              for j in range (16):
                  input_value[j] = input_data[j][k]

            
              input_value_scaled = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
             
              for i in range (16):
                  input_value_scaled[i] = input_value[i] / np.max(input_data[i])

              combined_input_value = np.array([input_value_scaled])

            # Realizar la predicción con la red neuronal

              output_value_scaled = model.predict(combined_input_value)

            # Desescalar el valor de salida para obtener el resultado final
              output_value = output_value_scaled * np.max(output_data)

            # Mostrar el resultado
              print("Resultado de la red neuronal para los valores de entrada ingresados:")
              print(output_value[0][0])  # Convertir el resultado a un número escalar


              valoress = int(output_value[0][0])
              valuerr.append(valoress)

    print(valuerr)


