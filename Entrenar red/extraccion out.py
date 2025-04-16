entrada = "datos_manual_2025-04-04.txt"
salida = "archivo_salida_simple.txt"
contador_filas = 0
valores = []

with open(entrada, 'r') as f_in:
    for linea in f_in:
        try:
            _, valor = linea.strip().split(" - ")
            valor = ''.join(c for c in valor if c.isdigit())
            if valor:
                valores.append(valor)
                contador_filas += 1
        except ValueError:
            continue

# Escribir todos los valores en una sola línea separados por comas
with open(salida, 'w') as f_out:
    f_out.write(','.join(valores))

print(f"¡Archivo procesado correctamente! Valores escritos: {contador_filas}")

