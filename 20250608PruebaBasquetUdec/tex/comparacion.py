import numpy as np
import matplotlib.pyplot as plt

# Leer archivos separados por coma (,)
def leer_voltajes_coma(nombre_archivo):
    voltajes = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            columnas = linea.split(',')
            if len(columnas) >= 2:
                try:
                    voltaje_str = columnas[1].replace('V', '').strip()
                    voltaje = float(voltaje_str)
                    voltajes.append(voltaje)
                except ValueError:
                    continue
    return np.array(voltajes)

# Leer archivo anterior separado por punto y coma (;)
def leer_voltajes_puntoycoma(nombre_archivo):
    voltajes = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            columnas = linea.split(';')
            if len(columnas) >= 1:
                try:
                    voltaje_str = columnas[0].replace('V', '').strip()
                    voltaje = float(voltaje_str)
                    voltajes.append(voltaje)
                except ValueError:
                    continue
    return np.array(voltajes)

# Rellenar hasta N muestras con NaN si es necesario
def rellenar_hasta_n(array, n):
    if len(array) < n:
        return np.pad(array, (0, n - len(array)), constant_values=np.nan)
    else:
        return array[:n]

# Archivos
archivo_paralelo = 'Paralelo.log'
archivo_serie = 'Serie.log'
archivo_anterior = 'impresora_flexografica2_copy.log'

# Leer los datos
voltajes_paralelo = leer_voltajes_coma(archivo_paralelo)
voltajes_serie = leer_voltajes_coma(archivo_serie)
voltajes_anterior = leer_voltajes_puntoycoma(archivo_anterior)

# Ajustar los arrays a máximo 435 muestras
max_muestras = 435
voltajes_paralelo = rellenar_hasta_n(voltajes_paralelo, max_muestras)
voltajes_serie = rellenar_hasta_n(voltajes_serie, max_muestras)
voltajes_anterior = rellenar_hasta_n(voltajes_anterior, max_muestras)

# Crear eje de muestras
muestras = np.arange(max_muestras)

# Graficar
plt.figure(figsize=(12, 6))
plt.plot(muestras, voltajes_paralelo, label='Paralelo', color='blue', alpha=0.7)
plt.plot(muestras, voltajes_serie, label='Serie', color='red', alpha=0.7)
plt.plot(muestras, voltajes_anterior, label='Medición Anterior', color='purple', alpha=0.7)

plt.xlabel('Número de muestra')
plt.ylabel('Voltaje (V)')
plt.title('Comparación de voltajes en las tres mediciones')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
