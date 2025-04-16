# archivo_entrada.txt → tu archivo original
# archivo_salida.txt → archivo limpio con solo los 16 valores por línea

entrada = "datos_recibidos_2025-04-04.txt"
salida = "archivo_salida.txt"
contador_filas = 0

with open(entrada, 'r') as f_in, open(salida, 'w') as f_out:
    for linea in f_in:
        try:
            # Separar la línea por el guion
            _, datos = linea.strip().split(" - ")
            # Separar los números, eliminar vacío al final si hay una coma extra
            numeros = [n for n in datos.strip().split(',') if n]

            # Asegurarse de que haya exactamente 16 números
            if len(numeros) == 16:
                f_out.write(','.join(numeros) + '\n')
                contador_filas += 1
        except ValueError:
            # Saltar líneas mal formateadas
            continue

print(f"¡Archivo procesado correctamente! Filas escritas: {contador_filas}")
