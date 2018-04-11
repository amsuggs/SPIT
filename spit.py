import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
#%load_ext autoreload
#%autoreload 2
import sys
import VersionZeroPointZero as PSS
import math
import scipy as sp
from scipy import signal

dispersionMeasure = 80
signal = PSS.Signal(TotTime = 50, bw = 40, SignalType = 'voltage', data_type = 'int16')
Psr1 = PSS.Pulsar(signal)
Psr1.make_pulses()

real = Psr1.signal[0,:]
imag = Psr1.signal[1,:]
toFile = np.zeros(2000, dtype=np.int8)

for i in range(0, 1000):
    j = 2 * i
    toFile[j] = np.int8(real[i])
    toFile[j+1] = np.int8(imag[i])

f = open('PulsarSignalOutputs/spit.bin', 'wb')
f.write(bytes(toFile))
f.close()




