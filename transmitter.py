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

# f_carrier in Hz
# x_bt input signal
def modulator(A_carrier, f_carrier, x_bt, f_sampling):
    # Time vector based on the sampling frequency and signal length
    t = np.arange(len(x_bt)) / f_sampling

    # Generate the modulated signal using vectorized operations
    x_mt = A_carrier * np.sin(2 * np.pi * f_carrier * t) * x_bt

    return x_mt

def transmitter(data, Tb, fs, A_carrier, f_carrier, f_pass, f_stop, A_pass, A_stop):    
    # Encode baseband signal
    bs = wcs.encode_string(data)
    xb = wcs.encode_baseband_signal(bs, Tb, fs)

    print("encoding done")

    # modulate
    xb_modulated = modulator(A_carrier, f_carrier, xb, fs)
    
    dmax = 5.0
    c = 340
    d = dmax*np.random.rand(1)
    m = int(np.round(d/c*fs))
    Nbuf = int(np.round(0.5*fs))
    xb_modulated = np.concatenate((xb_modulated, np.zeros(m+Nbuf)))

    print("modulation done")

    # bandlimit
    ellip_filter_b, ellip_filter_a = filter_bp(f_pass, f_stop, A_pass, A_stop, fs)
    xt = signal.lfilter(ellip_filter_b, ellip_filter_a, x=xb_modulated)

    # send
    sd.play(xt, fs , blocking=True)
    sd.wait()

    print("bandlimiting done")


def main():
    channel_id = 12
    Tb = 0.12  # 2 sidelobes, 1 sidelobe = 0.08
    fs = 35e3

    f_pass = (3475, 3525)
    f_stop = (3450, 3550)

    A_pass = 1  # passband ripples
    A_stop = 60  # stopband attenuation

    f_carrier = 3500
    A_carrier = 1  # amplitude of input signal

    # Create Signal
    
    # TODO: Add customizable arguments --> Detect input or set defaults
    # data = "a"
    data = "daffodilly"
    # data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sit amet aliquet felis. Nulla non tur"

    transmitter(data, Tb, fs, A_carrier, f_carrier, f_pass, f_stop, A_pass, A_stop)
    
    
if __name__ == "__main__":
    main()

    