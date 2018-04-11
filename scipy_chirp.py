import numpy as np
import scipy.signal
from scipy.signal import chirp, gausspulse
import matplotlib.pyplot
from matplotlib.pyplot import plot, subplot, pcolormesh, figure, title, xlabel, ylabel, grid, clf, show
import pickle
import datetime

#beginning frequency (Hz)
f0 = 100
#ending frequency (Hz)
f1 =25
#time to run sample (sec)
t1 = 1
#number of samples to take
nr_samples = 4096
#method in which to evaluate the chirp
chirp_method = "quadratic"
#create an array of size from '0' to 't1' split into 'nr_samples' indeces 
t = np.linspace(0, t1, nr_samples)

###CREATING A QUADRATIC CHIRP###
sig = chirp(t, f0=f0, f1=f1, t1=t1, method=chirp_method)
figure(figsize=[10, 4])
clf()
subplot(2,1,1)
title("Quadratic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1))
ylabel('Frequency (Hz)')
xlabel('time (sec)')
plot(t, sig)

subplot(2,1,2)
grid(True)
plot(t, f0 + (f1-f0)*t**2/t1**2, 'r')
show()

now = datetime.datetime.now()
file_str = "PulsarSignalOutputs/scipy_chirp_v0_true(%s).bin" % (now.isoformat())
file = open(file_str, "wb")
pickle.dump(sig, file)
file.close()

###CREATING A QUADRATIC CHIRP (VERTEX ZERO = FALSE)###
sig = chirp(t, f0=f0, f1=f1, t1=t1, method=chirp_method, vertex_zero=False)
figure(figsize=[10, 4])
clf()
subplot(2,1,1)
title("Quadratic Chirp, f(0)=%g, f(%g)=%g (Vertex_Zero = False)" % (f0, t1, f0))
ylabel('Frequency (Hz)')
xlabel('time (sec)')
plot(t, sig)

subplot(2,1,2)
grid(True)
plot(t, f1 - (f1-f0)*(t1-t)**2/t1**2, 'r')
show()

now = datetime.datetime.now()
file_str = "PulsarSignalOutputs/scipy_chirp_v0_false(%s).bin" % (now.isoformat())
file = open(file_str, "wb")
pickle.dump(sig, file)
file.close()