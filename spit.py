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

# print(Psr1.signal[0,:])
# print(bytes(Psr1.signal[0,:]))

psrSigFile = open('PulsarSignalOutputs/pulsarSignalFile.bin', 'wb')
psrSigFile.write(bytes(Psr1.signal[0,:]))
psrSigFile.close()




