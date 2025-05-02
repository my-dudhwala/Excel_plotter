import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Load Excel Data
file = 'Piezo_OpAmp.xlsx'
df = pd.read_excel(file)
ppg_raw = df.iloc[:, 0].values  # assuming data is in first column

data = df.iloc[:, 0].dropna().reset_index(drop=True)

# 1. Remove DC offset
ppg_centered = ppg_raw - ppg_raw.mean()

# 2. Apply Bandpass Filter (0.5–5 Hz for typical heart rates)
def bandpass_filter(data, lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, data)

# Example Sampling Rate (adjust if known)
fs = 100  # Hz
filtered_ppg = bandpass_filter(ppg_centered, 0.5, 5, fs)

# 3. Plotting
plt.figure(figsize=(12, 5))
plt.plot(filtered_ppg, label='Filtered PPG')
plt.title("Filtered PPG Signal")
plt.xlabel("Sample Number")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()