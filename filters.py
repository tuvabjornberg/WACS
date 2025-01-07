import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import ellip, ellipord, freqz

# Bandpass filter specifications
fs = 35000  # Sampling frequency (arbitrary, ensure it's much higher than max frequency)
fpass_bandpass = [3475, 3525]  # Passband frequencies (Hz)
fstop_bandpass = [3450, 3550]  # Stopband frequencies (Hz)
gpass_bandpass = 0.1  # Passband ripple (dB)
gstop_bandpass = 40  # Stopband attenuation (dB)

# Lowpass filter specifications
fpass_lowpass = 50  # Passband edge frequency (Hz)
fstop_lowpass = 75  # Stopband edge frequency (Hz)
gpass_lowpass = 0.1  # Passband ripple (dB)
gstop_lowpass = 40  # Stopband attenuation (dB)

# Normalize frequencies for Bandpass filter
wp_bandpass = np.array(fpass_bandpass) / (fs / 2)
ws_bandpass = np.array(fstop_bandpass) / (fs / 2)

# Normalize frequencies for Lowpass filter
wp_lowpass = fpass_lowpass / (fs / 2)
ws_lowpass = fstop_lowpass / (fs / 2)

# Design Bandpass filter
n_bandpass, wn_bandpass = ellipord(wp_bandpass, ws_bandpass, gpass_bandpass, gstop_bandpass)
b_bandpass, a_bandpass = ellip(n_bandpass, gpass_bandpass, gstop_bandpass, wn_bandpass, btype='band')

# Design Lowpass filter
n_lowpass, wn_lowpass = ellipord(wp_lowpass, ws_lowpass, gpass_lowpass, gstop_lowpass)
b_lowpass, a_lowpass = ellip(n_lowpass, gpass_lowpass, gstop_lowpass, wn_lowpass, btype='low')

# Frequency response for Bandpass filter
w_bandpass, h_bandpass = freqz(b_bandpass, a_bandpass, worN=8000)
frequencies_bandpass = w_bandpass * fs / (2 * np.pi)

# Frequency response for Lowpass filter
w_lowpass, h_lowpass = freqz(b_lowpass, a_lowpass, worN=8000)
frequencies_lowpass = w_lowpass * fs / (2 * np.pi)

# Create a single plot with subplots
fig, axs = plt.subplots(2, 1, figsize=(8, 8))

# Bandpass filter response plot
axs[0].plot(frequencies_bandpass, 20 * np.log10(abs(h_bandpass)), 'r', label='Magnitude Response')
axs[0].set_title('Bandpass Filter Response')
axs[0].set_xlabel('Frequency (Hz)')
axs[0].set_ylabel('Magnitude (dB)')
axs[0].set_xticks([fstop_bandpass[0], fpass_bandpass[0], 3500, fpass_bandpass[1], fstop_bandpass[1]], 
           [r'$f_{{stop,1}}={}$'.format(fstop_bandpass[0]), 
            r'$f_{{pass,1}}={}$'.format(fpass_bandpass[0]), 
            r'$f_c={}$'.format(3500), 
            r'$f_{{pass,2}}={}$'.format(fpass_bandpass[1]), 
            r'$f_{{stop,2}}={}$'.format(fstop_bandpass[1])])
axs[0].set_yticks([-gpass_bandpass, -gstop_bandpass], [r'$A_{{pass}}={}$'.format(gpass_bandpass), r'$A_{{stop}}={}$'.format(gstop_bandpass)])
axs[0].grid()

# Lowpass filter response plot
axs[1].plot(frequencies_lowpass, 20 * np.log10(abs(h_lowpass)), 'r', label='Magnitude Response')
axs[1].set_title('Lowpass Filter Response')
axs[1].set_xlabel('Frequency (Hz)')
axs[1].set_ylabel('Magnitude (dB)')
axs[1].set_xticks([0, fstop_lowpass, fpass_lowpass], [r'0', r'$f_{{stop}}={}$'.format(fstop_lowpass), r'$f_{{pass}}={}$'.format(fpass_lowpass)])
axs[1].set_yticks([-gpass_lowpass, -gstop_lowpass], [r'$A_{{pass}}={}$'.format(gpass_lowpass), r'$A_{{stop}}={}$'.format(gstop_lowpass)])
axs[1].grid()

# Adjust layout for better spacing
plt.tight_layout()

# Show plot
plt.show()

print(f'Sampling Frequency: {fs} Hz')
print(f'Bandpass Stopband Edge Frequency: {fstop_bandpass[0]} Hz')
print(f'Lowpass Stopband Edge Frequency: {fstop_lowpass} Hz')
