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
data_to_write = np.array([])
file_str = "OutputFiles/pss_complex_signal(%s).bin" % (now.isoformat())
#write data to a file as interleaved real and imaginary values
with open(file_str, 'wb') as file:
    for index in range(0, Psr1.phase.size):
        real = Psr1.signal[0][index]
        imag = Psr1.signal[1][index]
        data_to_write = np.append(data_to_write, complex(real, imag))
    pickle.dump(data_to_write, file)
    
plt.figure(figsize=[10,4])
plt.clf()
plt.subplot(3,1,1)
plt.title("Complex Pulsar Data representing voltage vs time.")
plt.ylabel("Voltage")
plt.xlabel("Time")
plt.plot(data_to_write.real)
plt.plot(data_to_write.imag)

plt.subplot(3,1,2)
plt.title("Raw Pulsar Data representing voltage vs time. Jones Vector Real Data")
plt.ylabel("Voltage")
plt.xlabel("Time")
plt.plot(data_to_write.real)

plt.subplot(3,1,3)
plt.title("Raw Pulsar Data representing voltage vs time. Jones Vector Imaginary Data")
plt.ylabel("Voltage")
plt.xlabel("Time")
plt.plot(data_to_write.imag)
plt.show()





