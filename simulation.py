#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation template for the wireless communication system project in Signals 
and Transforms.

For plain text inputs, run:
$ python3 simulation.py "Hello World!"

For binary inputs, run:
$ python3 simulation.py -b 010010000110100100100001

2020-present -- Roland Hostettler <roland.hostettler@angstrom.uu.se>
"""

""""
Modified by group 10:
Nora Reneland
Matilda Stenbaek
Tuva Björnberg
William Mårback
"""

import sys
import numpy as np
from scipy import signal

# import matplotlib.pyplot as plt
import wcslib as wcs

# f_pass and f_stop are input as tuples in Hz
# A_pass and A_stop are input in DB
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

# f_carrier in Hz
# x_bt input signal
def modulator(A_carrier, f_carrier, x_bt):
    w_carrier = 2 * np.pi * f_carrier

    x_mt = np.zeros(len(x_bt))
    for t in range(len(x_bt)):
        if x_bt[t] == 1:
            x_mt[t] = x_bt[t] * A_carrier * np.sin(w_carrier * t)
        elif x_bt[t] == -1:
            x_mt[t] = x_bt[t] * A_carrier * np.sin(w_carrier * t - np.pi)
        else:
            raise ValueError("Error: x_bt contains invalid values.")

    return x_mt

def demodulator(f_carrier, y, f_stop, A_pass, A_stop, f_sample):
    w_carrier = 2 * np.pi * f_carrier

    y_i_d = y * np.cos(w_carrier)
    y_q_d = -y * np.sin(w_carrier)

    lp_filter = filter_lp(f_carrier, f_stop, A_pass, A_stop, f_sample)
    
    y_i_d_filtered = signal.lfilter(lp_filter[0], lp_filter[1], x=y_i_d)
    y_q_d_filtered = signal.lfilter(lp_filter[0], lp_filter[1], x=y_q_d)
    
    return y_i_d_filtered + 1j*y_q_d_filtered

def main():
    # Parameters
    # TODO: Add your parameters here. You might need to add other parameters as
    # well.
    channel_id = 12
    Tb = 0.12  # 2 sidelobes, 1 sidelobe = 0.08
    fs = 35e3
    Ts = 1 / fs

    f_pass = (3475, 3525)
    f_stop = (3450, 3550)

    A_pass = 3  # passband ripples
    A_stop = 40  # stopband attenuation

    f_carrier = 3500
    A_carrier = 1  # amplitude of input signal

    # Detect input or set defaults
    string_data = True
    data = None
    if len(sys.argv) == 2:
        data = str(sys.argv[1])

    elif len(sys.argv) == 3 and str(sys.argv[1]) == "-b":
        string_data = False
        data = str(sys.argv[2])

    else:
        print("Warning: No input arguments, using defaults.", file=sys.stderr)
        data = "Hello World!"

    # Convert string to bit sequence or string bit sequence to numeric bit
    # sequence
    if string_data:
        bs = wcs.encode_string(data)
    else:
        bs = np.array([bit for bit in map(int, data)])

    # Encode baseband signal
    xb = wcs.encode_baseband_signal(bs, Tb, fs)

    # TODO: Put your transmitter code here (feel free to modify any other parts
    # too, of course)

    xb_modulated = modulator(A_carrier, f_carrier, xb)

    ellip_filter = filter_bp(f_pass, f_stop, A_pass, A_stop, fs)

    xt = signal.lfilter(ellip_filter[0], ellip_filter[1], x=xb_modulated)
    
    print("x")
    print(xb)
    print(xb_modulated)
    print(xt)
    
    # Channel simulation
    # TODO: Enable channel simulation.
    yr = wcs.simulate_channel(xt, fs, channel_id)

    # TODO: Put your receiver code here. Replace the three lines below, they
    # are only there for illustration and as an MWE. Feel free to modify any
    # other parts of the code as you see fit, of course.

    yb = signal.lfilter(ellip_filter[0], ellip_filter[1], x=yr)
    yb_demodulated = demodulator(f_carrier, yb, f_pass[1], A_pass, A_stop, fs)
    ybm = np.abs(yb_demodulated)
    ybp = np.angle(yb_demodulated)
    
    print("\ny")
    print(yb)
    print(yb_demodulated)
    print(ybm)
    print(ybp)
    
    # Example: 
    # yb = xb * np.exp(1j * np.pi / 5) + 0.1 * np.random.randn(xb.shape[0])
    # ybm = np.abs(yb)
    # ybp = np.angle(yb)

    # Baseband and string decoding
    br = wcs.decode_baseband_signal(ybm, ybp, Tb, fs)
    data_rx = wcs.decode_string(br)
    print("Received: " + data_rx)


if __name__ == "__main__":
    main()
