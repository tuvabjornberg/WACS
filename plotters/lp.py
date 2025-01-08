import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ellip, ellipord, freqz

# Specifications for Lowpass Filter
fs = 35000  # Sampling frequency (arbitrary, ensure it's much higher than max frequency)
fpass = 50  # Passband edge frequency (Hz)
fstop = 75  # Stopband edge frequency (Hz)
gpass = 0.1  # Passband ripple (dB)
gstop = 40  # Stopband attenuation (dB)

# Normalize frequencies
wp = fpass / (fs / 2)  # Passband normalized frequency
ws = fstop / (fs / 2)  # Stopband normalized frequency

# Design filter
n, wn = ellipord(wp, ws, gpass, gstop)
b, a = ellip(n, gpass, gstop, wn, btype='low')

# Frequency response
w, h = freqz(b, a, worN=8000)
frequencies = w * fs / (2 * np.pi)

# Plot
plt.figure(figsize=(8, 4))
plt.plot(frequencies, 20 * np.log10(abs(h)), 'r', label='Magnitude Response')
plt.title('Elliptic Low-Pass Filter Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xticks([0, fstop, fpass], [r'0', r'$f_{{stop}}={}$'.format(fstop), r'$f_{{pass}}={}$'.format(fpass)])
plt.yticks([-gpass, -gstop], [r'$A_{{pass}}={}$'.format(gpass), r'$A_{{stop}}={}$'.format(gstop)])
plt.grid()
plt.legend()
plt.show()

print(f'Sampling Frequency: {fs} Hz')
print(f'Stopband Edge Frequency: {fstop} Hz')
