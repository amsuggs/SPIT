import numpy as np
import matplotlib.pyplot as plt
import VersionZeroPointZero as PSS
import math as maths
import scipy as sp
from scipy import signal
import time
import pss_arg_parser as ap
import unit_exponent_parser as uep

params = ap.parse_args()  # Read in flags and arguments. Stored as dot-accessible members in a namespace.
vals = {}

# run all values through unit and exponent parser
def apply_unit_and_exponentiation():
    vals['freq'] = int(uep.apply_unit_and_exponents(params.frequency))
    vals['bandwidth'] = int(uep.apply_unit_and_exponents(params.bandwidth))
    vals['period'] = float(uep.apply_unit_and_exponents(params.period))
    if vals['period'] != params.period:
        vals['period'] *= 1000

    print(vals)

apply_unit_and_exponentiation()

# create a signal with the given parameters, or defaults.
Sig1 = PSS.Signal(f0 = vals['freq'], bw = vals['bandwidth'], TotTime = vals['period'], SignalType = 'voltage', data_type = 'int16')

# create a pulsar from that signal and then create pulses
Psr1 = PSS.Pulsar(Sig1)
Psr1.make_pulses()

# write files
now = time.strftime("%m.%d.%Y") + "-" + time.strftime("%H.%M.%S")
file_str = "OutputFiles/" + params.file + "(%s).bin" % now #append the datetime to the end of the file.

pulse = np.array([])
with open(file_str, 'wb') as file:
    for index in range(0, Psr1.phase.size):
        real = Psr1.signal[0][index]
        imag = Psr1.signal[1][index]
        p = np.complex64(real - 1j * imag)
        pulse = np.append(pulse, p)
    file.write(bytearray(pulse))
    file.close()

if params.plot:
    plt.figure(figsize=[10, 4])
    plt.clf()
    plt.subplot(3,1,1)
    plt.title("Complex Pulsar Data representing voltage vs time.")
    plt.ylabel("Voltage")
    plt.xlabel("Time")
    plt.plot(pulse.real)
    plt.plot(pulse.imag)

    plt.subplot(3, 1, 2)
    plt.title("Raw Pulsar Data representing voltage vs time. Jones Vector Real Data")
    plt.ylabel("Voltage")
    plt.xlabel("Time")
    plt.plot(pulse.real)

    plt.subplot(3,1,3)
    plt.title("Raw Pulsar Data representing voltage vs time. Jones Vector Imaginary Data")
    plt.ylabel("Voltage")
    plt.xlabel("Time")
    plt.plot(pulse.imag)
    plt.show()