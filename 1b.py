import numpy as np
import matplotlib.pyplot as plt

A_carrier = 1
f_carrier = 3500
w_carrier = 2 * np.pi * f_carrier
T_b = 280 / f_carrier  # M = 300
N = 1  # Number of rect pulses

# Time vector for x_b(t)
t = np.linspace(-3 * T_b, 3 * T_b, 1000)

# Frequency vector for plot
freqs = np.linspace(3400, 3600, 500) * 2 * np.pi


def X_b_w(T_b, N, w):  # nothing done for b_n
    X_b_w = np.zeros_like(t, dtype=complex)
    for n in range(N):
        delay = (2 * n + 1) * T_b / 2
        X_b_w += np.sinc(w * T_b / (2 * np.pi)) * np.exp(-1j * w * delay)
    return X_b_w


X_m_w = np.array(
    [A_carrier * 1j / 2 * (X_b_w(T_b, N, w + w_carrier) - X_b_w(T_b, N, w - w_carrier)) for w in freqs]
)

plt.plot(freqs / (2 * np.pi), np.abs(X_m_w))
plt.xlabel("Frequency (Hz)")
plt.xlim(3450, 3550)
plt.xticks([3475, 3500, 3525])
plt.ylabel("|Xm(ω)|")
plt.title("Magnitude Spectrum of Xm(ω)")
plt.grid()
plt.show()
