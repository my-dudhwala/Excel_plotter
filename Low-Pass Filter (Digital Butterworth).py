from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, cutoff, fs, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Parameters (adjust as needed)
fs = 1000  # Sampling frequency in Hz
cutoff = 10  # Desired cutoff frequency of the filter, in Hz
filtered = butter_lowpass_filter(data, cutoff, fs)

plt.figure(figsize=(10, 5))
plt.plot(data, alpha=0.5, label='Original', linestyle='--')
plt.plot(filtered, label='Butterworth Filtered', color='purple')
plt.title('Smoothed Arduino Data (Low-pass Filter)')
plt.xlabel('Sample Number')
plt.ylabel('Value')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()