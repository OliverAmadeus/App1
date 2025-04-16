import pandas as pd
import os
from datetime import date, datetime
import time

# Crear una lista con los nombres de los parámetros
parametros = ["Irradiancia", "Temperatura", "VoltajeIN", "CorrienteIN", "PotenciaIN", "PotenciaIN", "VoltajeOUT", "CorrienteOUT", "PotenciaOUT", "Ciclodetrabajo", "Hora"]

# Ruta de la carpeta que contiene los archivos txt
carpeta_valores = "VALORES"

# Crear la carpeta BaseDeDatos si no existe
carpeta_base_datos = "BaseDeDatos"
if not os.path.exists(carpeta_base_datos):
    os.makedirs(carpeta_base_datos)

while True:
    # Obtener la fecha actual y la hora actual
    fecha_actual = date.today().strftime("%Y-%m-%d")
    hora_actual = datetime.now().strftime("%H:%M:%S")
    nombre_archivo_excel = os.path.join(carpeta_base_datos, f"{fecha_actual}.xlsx")

    if os.path.exists(nombre_archivo_excel):
        # Si el archivo Excel ya existe, cargarlo
        df = pd.read_excel(nombre_archivo_excel)
        nuevo_dato = {}
        for parametro in parametros[:-1]:  # Excluir el parámetro "Hora"
            archivo = os.path.join(carpeta_valores, f"{parametro}.txt")
            with open(archivo, "r") as f:
                nuevo_dato[parametro] = float(f.read())
        # Agregar la hora actual a los datos
        nuevo_dato["Hora"] = hora_actual
        # Convertir cada valor de nuevo_dato en una lista
        nuevo_dato = {parametro: [valor] for parametro, valor in nuevo_dato.items()}
        # Agregar una nueva fila con los valores actuales
        df = pd.concat([df, pd.DataFrame(nuevo_dato)], ignore_index=True)
        # Guardar el DataFrame actualizado en el archivo Excel
        df.to_excel(nombre_archivo_excel, index=False)
    else:
        # Si el archivo Excel no existe, crear uno nuevo con los valores actuales
        datos = {}
        for parametro in parametros[:-1]:  # Excluir el parámetro "Hora"
            archivo = os.path.join(carpeta_valores, f"{parametro}.txt")
            with open(archivo, "r") as f:
                datos[parametro] = [float(f.read())]
        # Agregar la hora actual a los datos
        datos["Hora"] = [hora_actual]
        df = pd.DataFrame(datos)
        df.to_excel(nombre_archivo_excel, index=False)

    with open('VALORES/Temperatura.txt', 'r') as f:
         datos1 = float(f.read())

    with open('VALORES/Temperatura1.txt', 'a') as f:
        f.write(str(datos1) + ',' + '\n')

    #print(f"¡Archivo Excel actualizado con éxito ({fecha_actual}.xlsx)!")
    time.sleep(60)  # Esperar 60 segundos antes de la próxima iteración
