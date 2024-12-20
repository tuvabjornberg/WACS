import sys
import numpy as np
from scipy import signal
import wcslib as wcs
import sounddevice as sd

def filter_bp(f_pass, f_stop, A_pass, A_stop, f_sample):
    fn = f_sample / 2

    w_pass = [f / fn for f in f_pass]
    w_stop = [f / fn for f in f_stop]

    return signal.iirdesign(w_pass, w_stop, A_pass, A_stop, ftype="ellip")

def filter_lp(f_pass, f_stop, A_pass, A_stop, f_sample):
    fn = f_sample / 2

    w_pass = f_pass / fn
    w_stop = f_stop / fn

    return signal.iirdesign(w_pass, w_stop, A_pass, A_stop, ftype="ellip")


def demodulator(f_carrier, y, f_stop, A_pass, A_stop, f_sample):
    print(y)
    y = y[:, 0]
    print(y)

    t = np.arange(len(y)) / f_sample

    # Mix the received signal with in-phase and quadrature carriers
    y_i_d = y * np.cos(2 * np.pi * f_carrier * t)
    y_q_d = -y * np.sin(2 * np.pi * f_carrier * t)

    lp_filter_b, lp_filter_a = filter_lp(f_carrier, f_stop, A_pass, A_stop, f_sample)

    y_i_d_filtered = signal.lfilter(lp_filter_b, lp_filter_a, x=y_i_d)
    y_q_d_filtered = signal.lfilter(lp_filter_b, lp_filter_a, x=y_q_d)

    return y_i_d_filtered + 1j * y_q_d_filtered

def main():
    channel_id = 12
    Tb = 0.12  # 2 sidelobes, 1 sidelobe = 0.08
    fs = 35e3

    f_pass = (3475, 3525)
    f_stop = (3450, 3550)

    A_pass = 0.1  # passband ripples
    A_stop = 40  # stopband attenuation

    f_carrier = 3500
    A_carrier = 1  # amplitude of input signal

    expected = "Hello World!"
    expected_bits = wcs.encode_string(expected)

    ellip_filter_b, ellip_filter_a = filter_bp(f_pass, f_stop, A_pass, A_stop, fs)
    
    y = sd.rec(int(20* fs), fs, channels=1, blocking=True)
    sd.wait()
    print("Recording done")

    yb = signal.lfilter(ellip_filter_b, ellip_filter_a, x=y)
    print("bandlimiting done")

    yb_demodulated = demodulator(f_carrier, yb, f_pass[1], A_pass, A_stop, fs)
    ybm = np.abs(yb_demodulated)
    ybp = np.angle(yb_demodulated)
    print("demodulation done")

    br = wcs.decode_baseband_signal(ybm, ybp, Tb, fs)
    # print(br)

    print("Expected bits:" + str(len(expected_bits)))
    counter = 0
    for i in range(len(expected_bits)-1):
        if not (expected_bits[i] == 1 and br[i] == True or expected_bits[i] == 0 and br[i] == False):
            counter+=1
    
    print("Incorrect bits: " + str(counter))
    data_rx = wcs.decode_string(br)
    print("Received: " + data_rx)

if __name__ == "__main__":
    main()
    