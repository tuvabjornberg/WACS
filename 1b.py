import numpy as np
import matplotlib.pyplot as plt

# Define parameters
Tb = 0.0001  # Width of the baseband pulse in seconds
f_c = 3500  # Carrier frequency in Hz
w_c = 2 * np.pi * f_c  # Carrier angular frequency in rad/s

# Frequency range (omega values)
omega = np.arange(-5 * w_c, 5 * w_c, 0.5)

# Define X_b(omega) as a sinc function (assuming a pulse of width Tb)
X_b = lambda omega_2: Tb * np.sinc(omega_2 * Tb / (2 * np.pi))

# Calculate the expression j/2 * (X_b(omega) * (omega + w_c) - X_b(omega) * (omega - w_c))
j_over_2 = 1j / 2
expression = j_over_2 * (X_b(omega + w_c) - X_b(omega - w_c))

# Plotting the real and imaginary parts of the expression
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(omega, expression.real, label="Real Part", color="blue")
plt.title("Real Part of the Expression")
plt.xlabel("Frequency (rad/s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(omega, expression.imag, label="Imaginary Part", color="red")
plt.title("Imaginary Part of the Expression")
plt.xlabel("Frequency (rad/s)")
plt.ylabel("Amplitude")
#plt.xlim(-5000, 5000)
plt.grid(True)

plt.tight_layout()
plt.show()
