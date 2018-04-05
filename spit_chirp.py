import numpy as np
import matplotlib.pyplot as plt
import math as mt
import pickle
import datetime

def quad_chirp(nr_samples, amp=1.0, f0=0, f1=100, t1=1, phi=0):
    t=np.linspace(0,t1,nr_samples)
    ft = f0 + (f1-f0)*t**2/t1**2
    sig = amp*np.cos(2*np.pi*ft*t + phi)
    
    plt.figure(figsize=[10,4])
    plt.clf()
    plt.subplot(2,1,1)
    plt.title("Quadratic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1))
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('time (sec)')
    plt.plot(t, sig)
    
    plt.subplot(2,1,2)
    plt.grid(True)
    plt.plot(t, f0 + (f1-f0)*t**2/t1**2, 'r')
    plt.show()
    
    now = datetime.datetime.now()
    file_str = "PulsarSignalOutputs/spit_chirp(%s).bin" % (now.isoformat())
    file = open(file_str, "wb")
    pickle.dump(sig, file)
    file.close()
    
    return sig
    
    
chirp = quad_chirp(nr_samples=4096, f0=100, f1=25)