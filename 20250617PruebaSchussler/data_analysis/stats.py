archivo = "extract_serie"
voltajes = []

with open(archivo, "r") as f:
    for linea in f:
        if linea.strip():
            partes = linea.strip().split(",")
            voltajes.append(float(partes[0]))

minimo = min(voltajes)
maximo = max(voltajes)
media = sum(voltajes) / len(voltajes)

print(f"Voltaje mínimo: {minimo:.4f} V")
print(f"Voltaje máximo: {maximo:.4f} V")
print(f"Voltaje medio:  {media:.4f} V")
