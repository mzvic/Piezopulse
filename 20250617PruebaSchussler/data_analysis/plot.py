import matplotlib.pyplot as plt

voltajes = []

with open("putty.log","r") as f:
    for linea in f:
        if linea.strip():  
            partes = linea.strip().split(",")
            voltajes.append(float(partes[0]))
muestras = list(range(len(voltajes)))

plt.plot(muestras, voltajes, marker="o")
plt.xlabel("Muestra")
plt.ylabel("Voltaje (V)")
plt.grid(True)
plt.show()
