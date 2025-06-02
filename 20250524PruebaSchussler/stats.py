from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Open and read the log file
with open("impresora_flexografica2.log", "r") as file:
    lines = file.readlines()
    data = []
    for line in lines:
        if line.strip():  # Check if the line is not empty
            parts = line.split(";")
            if len(parts) == 4:  # Ensure there are exactly 4 parts
                try:
                    # Convert Vpiezo to absolute value and multiply by 1000
                    Vpiezo = abs(float(parts[0].strip()) * 1000)
                    AccelX = float(parts[1].strip())
                    AccelY = float(parts[2].strip())
                    AccelZ = float(parts[3].strip())
                    data.append([Vpiezo, AccelX, AccelY, AccelZ])
                except ValueError:
                    print(f"Error converting line to float: {line.strip()}")

# Create a DataFrame from the processed data
df = DataFrame(data, columns=["Vpiezo", "AccelX", "AccelY", "AccelZ"])

# Calculate statistics for the DataFrame
stats = {
    "mean": df.mean(),
    "std": df.std(),
    "min": df.min(),
    "max": df.max(),
    "median": df.median(),
}

# Create a DataFrame for the statistics
stats_df = pd.DataFrame(stats)

# Print the statistics to the console
print("Statistics:")
print(stats_df)

# --- Plotting Section ---
plt.figure(figsize=(12, 6)) # Increased height slightly for better visibility

# Plot both normalized signals on the same scale
# AccelZ is standardized (mean-subtracted and divided by std dev)
plt.plot((df["AccelZ"] - df["AccelZ"].mean()) / df["AccelZ"].std(), label="AccelZ (estandarizado)", color="orange", alpha=0.8)
# Vpiezo is normalized (divided by its max value)
plt.plot(df["Vpiezo"] / df["Vpiezo"].max(), label="Vpiezo (normalizado)", color="blue", alpha=0.8)

# --- Identify and plot vertical lines when both signals are increasing ---

# Calculate the difference between consecutive values for Vpiezo and AccelZ
# A positive difference indicates an increase
vpiezo_increasing = df["Vpiezo"].diff() > 0
accelz_increasing = df["AccelZ"].diff() > 0

# Find the indices where both Vpiezo and AccelZ are increasing
# The '&' operator performs element-wise logical AND
both_increasing_indices = df.index[vpiezo_increasing & accelz_increasing]

# Plot vertical lines at these identified indices
for idx in both_increasing_indices:
    # Use plt.axvline to draw a vertical line at each increasing point
    # 'ls' for linestyle (e.g., '--' for dashed), 'color' for line color, 'alpha' for transparency
    
    plt.axvline(x=idx, color='green', linestyle=':', alpha=0.4, label='Ambos aumentan' if idx == both_increasing_indices[0] else "")
print(f"Número de puntos donde ambos aumentan: {len(both_increasing_indices)}")
# print(f"Primeros 10 índices donde ambos aumentan: {both_increasing_indices[:10].tolist()}") # Descomentar para ver los primeros índices
# Add labels and title to the plot
plt.title("Comparación temporal entre Vpiezo y AccelZ con puntos de aumento simultáneo")
plt.xlabel("Muestras")
plt.ylabel("Señal normalizada")
plt.legend() # Display the legend for all plotted lines and markers
plt.grid(True) # Show a grid for better readability
plt.tight_layout() # Adjust plot parameters for a tight layout
plt.show() # Display the plot
