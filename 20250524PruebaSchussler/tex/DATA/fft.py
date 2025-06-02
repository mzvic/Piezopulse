from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Read and parse data
with open("impresora_flexografica2.log", "r") as file:
    lines = file.readlines()
    data = []
    for line in lines:
        if line.strip():
            parts = line.split(";")
            if len(parts) == 4:
                try:
                    Vpiezo = abs(float(parts[0].strip()))
                    AccelX = float(parts[1].strip())
                    AccelY = float(parts[2].strip())
                    AccelZ = float(parts[3].strip())
                    data.append([Vpiezo, AccelX, AccelY, AccelZ])
                except ValueError:
                    continue

# Create DataFrame
df = DataFrame(data, columns=["Vpiezo", "AccelX", "AccelY", "AccelZ"])

# Sampling frequency
fs = 100  # Hz
n = len(df)

# Function to plot FFT of a single signal in its own window and show top peaks
def plot_single_fft(signal, label, fs, num_peaks=3):
    """
    Plots the FFT of a single signal in a separate window and highlights the top N peaks.
    
    Args:
        signal (array-like): The signal data
        label (str): Name of the signal (for title/labels)
        fs (int): Sampling frequency in Hz
        num_peaks (int): Number of top peaks to highlight
    """
    plt.figure(figsize=(10, 5))
    
    centered = signal - signal.mean()  # Remove DC component
    fft_vals = np.fft.fft(centered)
    freqs = np.fft.fftfreq(n, d=1/fs)
    pos_mask = freqs > 0

    # Get positive frequencies and corresponding magnitudes
    positive_freqs = freqs[pos_mask]
    magnitudes = np.abs(fft_vals[pos_mask])

    plt.plot(positive_freqs, magnitudes, label=f"FFT of {label}")

    # Find peaks
    min_prominence = 0.05 * np.max(magnitudes)
    peaks, properties = find_peaks(magnitudes, prominence=min_prominence)

    # Sort peaks by their magnitude and select the top N
    if len(peaks) > 0:
        peak_magnitudes = magnitudes[peaks]
        sorted_peak_indices = np.argsort(peak_magnitudes)[::-1]
        top_n_peaks_indices = sorted_peak_indices[:num_peaks]
        top_n_peaks = peaks[top_n_peaks_indices]

        # Plot top N peaks as red dots
        plt.plot(positive_freqs[top_n_peaks], magnitudes[top_n_peaks], 
                "o", color='red', markersize=8, label=f"Top {num_peaks} Peaks")
        
        # Annotate the frequency of the top peaks
        for peak_idx in top_n_peaks:
            plt.text(positive_freqs[peak_idx], magnitudes[peak_idx],
                    f'{positive_freqs[peak_idx]:.2f} Hz',
                    fontsize=10, ha='center', va='bottom', color='red')

    plt.title(f"FFT of {label}")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

# Plot each signal in separate windows
plot_single_fft(df["AccelX"], "AccelX", fs, num_peaks=1)
plot_single_fft(df["AccelY"], "AccelY", fs, num_peaks=1)
plot_single_fft(df["AccelZ"], "AccelZ", fs, num_peaks=1)