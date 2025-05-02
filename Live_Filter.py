import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Configuration
port = 'COM12'       # Change this to your Arduino COM port
baud_rate = 115200    # Match with Arduino's Serial.begin(9600)
fs = 450            # Sampling frequency (Hz)
cutoff = 30         # Low-pass cutoff frequency (Hz)
order = 4
buffer_size = 450   # Number of samples to display/filter at once (e.g., 1 second window)

# Setup Butterworth filter
def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

# Connect to Arduino
ser = serial.Serial(port, baud_rate, timeout=1)
print(f"Connected to {port} at {baud_rate} baud.")

# Data containers
raw_data = []

plt.ion()  # Interactive mode on
fig, ax = plt.subplots(figsize=(10, 5))
line1, = ax.plot([], [], 'r--', alpha=0.2, label='Raw')
line2, = ax.plot([], [], 'purple', label='Filtered')
ax.set_ylim(0, 1023)  # Adjust if using analogRead()
ax.set_xlim(0, buffer_size)
ax.set_title("Real-time Arduino Data (Butterworth Filtered)")
ax.set_xlabel("Sample Number")
ax.set_ylabel("Value")
ax.grid(True)
ax.legend()

while True:
    try:
        line = ser.readline().decode().strip()
        if line.isdigit():
            value = int(line)
            raw_data.append(value)
            if len(raw_data) > buffer_size:
                raw_data.pop(0)

                # Filter when enough data is available
                filtered = butter_lowpass_filter(np.array(raw_data), cutoff, fs, order)

                # Update plot
                line1.set_data(range(buffer_size), raw_data)
                line2.set_data(range(buffer_size), filtered)
                ax.draw_artist(ax.patch)
                ax.draw_artist(line1)
                ax.draw_artist(line2)
                fig.canvas.flush_events()
                fig.canvas.draw()
    except KeyboardInterrupt:
        print("\nStopped by user.")
        break
    except Exception as e:
        print("Error:", e)

ser.close()