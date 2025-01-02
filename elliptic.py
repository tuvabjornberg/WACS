import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ellip, ellipord, freqz

# Specifications
fs = 35000  # Sampling frequency (arbitrary, ensure it's much higher than max frequency)
fpass = [3475, 3525]  # Passband frequencies (Hz)
fstop = [3450, 3550]  # Stopband frequencies (Hz)
gpass = 3  # Passband ripple (dB)
gstop = 40  # Stopband attenuation (dB)

# Normalize frequencies
wp = np.array(fpass) / (fs / 2)
ws = np.array(fstop) / (fs / 2)

# Design filter
n, wn = ellipord(wp, ws, gpass, gstop)
b, a = ellip(n, gpass, gstop, wn, btype='band')

# Frequency response
w, h = freqz(b, a, worN=8000)
frequencies = w * fs / (2 * np.pi)

# Plot
plt.figure(figsize=(8, 4))
plt.plot(frequencies, 20 * np.log10(abs(h)), 'r', label='Magnitude Response')
plt.axvline(fpass[0], color='k', linestyle='--', label='Passband')
plt.axvline(fpass[1], color='k', linestyle='--')
plt.axvline(fstop[0], color='b', linestyle='--', label='Stopband')
plt.axvline(fstop[1], color='b', linestyle='--')
plt.axhline(-gpass, color='g', linestyle='--', label='Passband Ripple')
plt.axhline(-gstop, color='orange', linestyle='--', label='Stopband Attenuation')
plt.title('Elliptic Band-Pass Filter Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid()
plt.legend()
plt.show()
