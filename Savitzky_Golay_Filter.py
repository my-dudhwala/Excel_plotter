from scipy.signal import savgol_filter

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = 'Piezo_OpAmp.xlsx'
df = pd.read_excel(file_path)

# Assume data is in the first column
data = df.iloc[:, 0].dropna().reset_index(drop=True)


# window_length must be odd and less than len(data)
smoothed = savgol_filter(data, window_length=11, polyorder=2)

plt.figure(figsize=(10, 5))
plt.plot(data, alpha=0.5, label='Original', linestyle='--')
plt.plot(smoothed, label='Savitzky-Golay Smoothed', color='green')
plt.title('Smoothed Arduino Data (Savitzky-Golay)')
plt.xlabel('Sample Number')
plt.ylabel('Value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()