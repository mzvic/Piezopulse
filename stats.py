# genera un reporte de datos estadísticos con el archivo impresora_flexografica.log. que contiene este formato Vpiezo ; AccelX ; AccelY ; AccelZ

from pandas import DataFrame
import pandas as pd
import numpy as np

with open("impresora_flexografica2.log", "r") as file:
    lines = file.readlines()
    data = []
    for line in lines:
        if line.strip():  # Check if the line is not empty
            parts = line.split(";")
            if len(parts) == 4:  # Ensure there are exactly 4 parts
                try:
                    Vpiezo = abs(float(parts[0].strip()))
                    AccelX = float(parts[1].strip())
                    AccelY = float(parts[2].strip())
                    AccelZ = float(parts[3].strip())
                    data.append([Vpiezo, AccelX, AccelY, AccelZ])
                except ValueError:
                    print(f"Error converting line to float: {line.strip()}")
    # Create a DataFrame from the data
    df = DataFrame(data, columns=["Vpiezo", "AccelX", "AccelY", "AccelZ"])
    # Calculate statistics
    stats = {
        "mean": df.mean(),
        "std": df.std(),
        "min": df.min(),
        "max": df.max(),
        "median": df.median(),
    }
    # Create a DataFrame for the statistics
    stats_df = pd.DataFrame(stats)
    # Save the statistics to a CSV file
    stats_df.to_csv("statistics.csv", index=True)
    # Print the statistics
    print("Statistics:")
    print(stats_df)
