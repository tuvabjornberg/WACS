import numpy as np
import matplotlib.pyplot as plt

# Define parameters
f_c = 3500  # Carrier frequency in Hz
w_c = 2 * np.pi * f_c  # Carrier angular frequency in rad/s
n = 1
M = 2
Tb = 5 / f_c  # Width of the baseband pulse in seconds

# Frequency range (omega values)
omega = np.arange(-5 * w_c, 5 * w_c, 0.5)

# Define X_b(omega) as a sinc function (assuming a pulse of width Tb)
def X_b(omega_2):
    return Tb * np.sinc(omega_2 * Tb / (2 * np.pi)) * \
                        np.exp(-1j * omega_2 * ((2 * n + 1) * Tb) / 2)

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
plt.xlim(-5000, 5000)
plt.grid(True)

plt.tight_layout()
plt.show()
