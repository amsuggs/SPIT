import numpy as np
import math

# # of Period Bins
p = 1024

#Bandwidth ~40 MHz
bw = 40.0

#Frequency ~400 MHz
f = 400.0

# Delta Time ~1 sec/ 40 sample
dt = 1.0/f

#Dispersion Measure
dm = 1.0/(math.pow(f, 2.0))

file = open('PulsarSignalOutputs/spyt.bin', 'wb')
for bin in range(0, p):
    x = 2 * math.pi * bin / p
    real = math.sin(x)
    imag = math.cos(x)
    file.write(np.int8(real * 100))
    file.write(np.int8(imag * 100))
    print(x)
    print(real * 100)
    print(imag * 100)
    print("---")
file.close()