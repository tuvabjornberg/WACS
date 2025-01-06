import numpy as np
import matplotlib.pyplot as plt

frequency_band = [3475, 3525]
A_carrier = 1
f_carrier = (frequency_band[0] + frequency_band[1]) / 2
w_carrier = 2 * np.pi * f_carrier
bandwidth = frequency_band[1] - frequency_band[0]
T_b_1 = 4 / bandwidth  # 0.08
T_b_2 = 6 / bandwidth  # 0.12
N = 1  # Number of rect pulses

# Time vector for x_b(t)
t1 = np.linspace(-3 * T_b_1, 3 * T_b_1, 1000)
t2 = np.linspace(-3 * T_b_2, 3 * T_b_2, 1000)

# Frequency vector for plot
freqs = np.linspace(3400, 3600, 500) * 2 * np.pi


def X_b_w(T_b, N, w, t):  # nothing done for b_n
    X_b_w = np.zeros_like(t, dtype=complex)
    for n in range(N):
        delay = (2 * n + 1) * T_b / 2
        X_b_w += np.sinc(w * T_b / (2 * np.pi)) * np.exp(-1j * w * delay)
    return X_b_w


X_m_w_1 = np.array(
    [
        A_carrier
        * 1j
        / 2
        * (X_b_w(T_b_1, N, w + w_carrier, t1) - X_b_w(T_b_1, N, w - w_carrier, t1))
        for w in freqs
    ]
)

X_m_w_2 = np.array(
    [
        A_carrier
        * 1j
        / 2
        * (X_b_w(T_b_2, N, w + w_carrier, t2) - X_b_w(T_b_2, N, w - w_carrier, t2))
        for w in freqs
    ]
)

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(freqs / (2 * np.pi), np.abs(X_m_w_1))
plt.xlabel("Frequency (Hz)")
plt.ylabel("|Xm(ω)|")
plt.xlim(3450, 3550)
plt.xticks([3475, 3500, 3525])
plt.title("Magnitude Spectrum of Xm(ω) with one sidelobe")
plt.grid()

plt.subplot(1, 2, 2)
plt.plot(freqs / (2 * np.pi), np.abs(X_m_w_2))
plt.xlabel("Frequency (Hz)")
plt.ylabel("|Xm(ω)|")
plt.xlim(3450, 3550)
plt.xticks([3475, 3500, 3525])
plt.title("Magnitude Spectrum of Xm(ω) with two sidelobes")
plt.grid()

plt.tight_layout()
plt.savefig("Sidelobes")
plt.show()
