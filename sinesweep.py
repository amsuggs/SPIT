import numpy as np
import math as maths
import scipy.signal
from scipy.signal import chirp, spectrogram, gausspulse
import scipy
from scipy import signal
import matplotlib.pyplot as plt

#frequency at time t0
beg_freq = 1500
#frequency of the waveform at time t1
end_freq = 250
#amount of time in seconds to run the sample
chirp_time = 10
#number of samples to take in the given time
chirp_samples = 8000
#method in which to evaluate the chirp
chirp_method = "quadratic"

#creates an array of size "samples" evenly spaced from 0 to time.
t1 = np.linspace(0, chirp_time, chirp_samples*chirp_time)
#create a quadratic chirp from 40 hz to 0 hz over 10 scds.
sig = chirp(t1, f0=beg_freq, f1=end_freq, t1=chirp_time, method=chirp_method, vertex_zero=False)
plt.title('Quadratic Chirp, f(0)=%d, f(10)=%d\n (vertex_zero=False)' % (beg_freq, end_freq))
plt.xlabel('Time (sec)')
plt.ylabel('Frequency (Hz)')
plt.plot(sig)
plt.show()

#number of points to plot per segment
pts_per_seg = 512
#points to overlap per segment
pts_to_overlap = 256
#length of the fft used
fft_len = 2048
#create a spectrogram, ff => sample frequencies, tt => segment times, Sxx = spectrogram of x
ff, tt, Sxx = spectrogram(sig, fs=chirp_samples, noverlap=pts_to_overlap, nperseg=pts_per_seg, nfft=fft_len)
plt.pcolormesh(tt, ff[:513], Sxx[:513])
plt.title('Quadratic Chirp Spectrogram, f(0)=%d, f(10)=%d\n (vertex_zero=False)' % (beg_freq, end_freq))
plt.xlabel('Time (sec)')
plt.ylabel('Frequency (Hz)')
plt.grid()
plt.show()

#sample time for a pulse 
sample_time = 2
#central frequency
cent_freq = 5
#fraction bandwidth
#frac_band =
#reference level at which frac_band is calculated (dB)
#frac_band_ref
t2 = np.linspace(-1.0, 1.0, 2 * 100, endpoint=False)
real, imag, env = signal.gausspulse(t2, fc=cent_freq, retquad=True, retenv=True)
plt.plot(t2, real, imag, env, t2, env, '--')
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
    