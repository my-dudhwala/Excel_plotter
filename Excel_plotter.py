import pandas as pd
import matplotlib.pyplot as plt

# Load Excel file
file_path = 'Piezo_OpAmp.xlsx'  # Change this to your actual file path
sheet_name = 0  # Or sheet name as string if known

# Read the data
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Assuming data is in the first column
column_name = df.columns[0]  # Get the name of the first column
data = df[column_name]

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(data, label='Arduino Data')
plt.title('Arduino Serial Data Waveform')
plt.xlabel('Sample Number')
plt.ylabel('Value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()