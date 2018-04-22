import numpy as np
import matplotlib.pyplot as plt
import sys
import VersionZeroPointZero as PSS
import math as maths
import scipy as sp
from scipy import signal
import pickle
import datetime
import pss_arg_parser as ap

params = ap.parse_args()#Read in flags and arguments. Stored as dot-accessible members in a namespace.

#create a signal with the given parameters, or defaults.
Sig1 = PSS.Signal(f0 = int(params.frequency), bw = int(params.bandwidth), TotTime = int(params.period), SignalType = 'voltage', data_type = 'int16')

#create a pulsar from that signal and then create pulses
Psr1 = PSS.Pulsar(Sig1)
Psr1.make_pulses()
  
    # cast to int32, maybe float32???
now = datetime.datetime.now()
pulse = np.array([])
file_str = "OutputFiles/pss_complex_signal.bin"
#write data to a file as interleaved real and imaginary values
with open(file_str, 'wb') as file:
    for index in range(0, Psr1.phase.size):
        real = Psr1.signal[0][index]
        imag = Psr1.signal[1][index]
        p1 = real + 1j * imag
        pulse = np.append(pulse, np.complex64(p1))
    file.write(bytearray(pulse))
    file.close()
    
plt.clf()
plt.subplot(3,1,1)
plt.title("Complex Pulsar Data representing voltage vs time.")
plt.ylabel("Voltage")
plt.xlabel("Time")
plt.plot(pulse.real)
plt.plot(pulse.imag)

plt.subplot(3,1,2)
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