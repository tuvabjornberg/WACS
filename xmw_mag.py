import numpy as np
import matplotlib.pyplot as plt

# Parameters
wc = 3500  # Center frequency (Hz)
f = np.linspace(-7000, 7000, 1000)  # Frequency range

# Sinc functions (normalize by pi for np.sinc)
sinc1 = np.sinc((f - wc) / 1000)  # Divide by 1000 to normalize to \(\pi\)
sinc2 = np.sinc((f + wc) / 1000)

# Plot
plt.plot(f, np.abs(sinc1), label=r'$\omega_c$', color='blue')
plt.plot(f, np.abs(sinc2), label=r'$-\omega_c$', color='red')
plt.title("Magnitude Spectra of Two Sinc Functions")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xticks([-wc, 0, wc], [r'$-\omega_c$', r'0', r'$\omega_c$'])
#plt.legend()
plt.grid()
plt.show()
