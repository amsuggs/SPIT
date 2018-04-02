import numpy as np
import math as maths
import scipy.signal
from scipy.signal import chirp, gausspulse
import scipy
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, subplot, pcolormesh, figure, title, xlabel, ylabel, grid, clf, show
import pickle
import datetime

#frequency at time t0
beg_freq = 20
#frequency of the waveform at time t1
end_freq =-20
#amount of time in seconds to run the sample
chirp_len = 10
#number of samples to take in the given time
chirp_samples = 1024
#method in which to evaluate the chirp
chirp_method = "quadratic"
fig_size=[10, 4]
t = np.linspace(0, chirp_len, chirp_samples)

###CREATING A QUADRATIC CHIRP###
sig = chirp(t, f0=beg_freq, f1=end_freq, t1=chirp_len, method=chirp_method)
figure(figsize=fig_size)
clf()
subplot(2,1,1)
title("Quadratic Chirp, f(0)=%g, f(%g)=%g" % (beg_freq, chirp_len, end_freq))
ylabel('Frequency (Hz)')
xlabel('time (sec)')
plot(t, sig)

subplot(2,1,2)
grid(True)
plot(t, beg_freq + (end_freq-beg_freq)*t**2/chirp_len**2, 'r')
show()

now = datetime.datetime.now()
file_str = "PulsarSignalOutputs/quadratic_chirp_v0_true(%g.%g.%g).bin" % (now.year, now.month, now.day)
file = open(file_str, "wb")
pickle.dump(sig, file)
file.close()

###CREATING A QUADRATIC CHIRP (VERTEX ZERO = FALSE)###
sig = chirp(t, f0=beg_freq, f1=end_freq, t1=chirp_len, method=chirp_method, vertex_zero=False)
figure(figsize=fig_size)
clf()
subplot(2,1,1)
title("Quadratic Chirp, f(0)=%g, f(%g)=%g (Vertex_Zero = False)" % (beg_freq, chirp_len, end_freq))
ylabel('Frequency (Hz)')
xlabel('time (sec)')
plot(t, sig)

subplot(2,1,2)
grid(True)
plot(t, end_freq - (end_freq-beg_freq)*(chirp_len-t)**2/chirp_len**2, 'r')
show()

now = datetime.datetime.now()
file_str = "PulsarSignalOutputs/quadratic_chirp_v0_false(%g.%g.%g).bin" % (now.year, now.month, now.day)
file = open(file_str, "wb")
pickle.dump(sig, file)
file.close()

#Central frequency for a pulse
cent_freq = 1400
t = np.linspace(-1, 1, chirp_len * chirp_samples, endpoint=False)
real, imag, env = signal.gausspulse(t, fc=cent_freq, retquad=True, retenv=True)
plt.plot(t, real, t, imag, t, env, '--')
plt.show()

#####params#####
# start => the starting frequency 
# finish => the finishing frequency
# seconds => the obserging time
# sample_rate => how many times we want to sample in the given time
# amplitude => 
# initial_phase => 
# dc =>

#def sinesweep(start, finish, seconds, samples, amplitude, phase, dc):
#    R = (finish / start) ** (1 / seconds)
#    B = 2 * maths.pi * start / maths.log(R)
#    A = phase - B
#    
#    time = np.array([])
#    index = 0
#    bin = 1 / samples
#    for index in range(0, seconds, bin):
#        time = np.append(time, index)
#
#    total = np.power((A + B * R), time)
#    return amplitude * np.sin(total) + dc
#    
#st = 0
#fn = 40000
#sd = 30
#sp = 1000
#ap = 0.2
#ps = maths.pi
#dc = 0.25
#
#signal = sinesweep(st, fn, sd, sp, ap, ps, dc)
    