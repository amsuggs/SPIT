import numpy as np
import matplotlib.pyplot as plt
import math
import pickle
import datetime
import spit_arg_parser as ap

params = ap.parse_args() #Read in flags and arguments. Stored as dot-accessible members in a namespace.
#Used in the quad_chirp call at the end of the file using the parameters gathered from the argument parser.

#Generates a quadratic chirp. Takes in number of samples, amplitude, 
#starting frequency, ending frequency, sample time, and pulse offset.
#nr_samples should be twice the highest frequecy.
def quad_chirp(nr_samples=int(params.samples), amp=float(params.amplitude), f0=int(params.begin), f1=int(params.end), t1=int(params.period), phi=int(params.offset)):
    #Calculation section.
    t1 = float(t1)/1000
    t=np.linspace(0,t1,nr_samples/t1) #Array of samples.
    beta = (f1 - f0) / (t1 ** 2) #Change between start and end frequencies.
    ft = f1 * t + beta * ((t1 - t) ** 3 - t1 ** 3) / 3 #Instantaneous frequency. Array.
    real = np.cos(2*np.pi*ft + phi) #Real component of the chirp.
    imag = np.sin(2*np.pi*ft + phi) #Imaginary component of the chirp.
    sig = amp*(real - 1j * imag) #Output signal. Real and imaginary components combined.
    
    #Plotting section.
#    plt.clf()
#    plt.subplot(1,1,1)
#    plt.title("Quadratic Chirp, f(0)=%g, f(%g)=%g" % (f0, t1, f1))
#    plt.ylabel('Amplitude')
#    plt.xlabel('time (sec)')
#    plt.plot(t, sig.real)
#    plt.plot(t, sig.imag)
#    plt.show()
    
    gauss_pulse(chirp = sig, x = t) #Gauss pulse generation
    
def gauss_pulse(chirp, x, mean=int(params.peak), std_dev=int(params.width)):
    mean = float(mean)/1000
    std_dev = float(std_dev)/1000
    gauss = (1/math.sqrt(2*math.pi*std_dev**2))*(math.e**(-(x-mean)**2/(2*std_dev**2)))
    real = chirp.real*gauss
    imag = chirp.imag*gauss
    pulse = np.complex64(real - 1j * imag)
    
    #Plotting section.
#    plt.clf()
#    plt.subplot(1,1,1)
#    plt.title("Gaussian pulse")
#    plt.plot(pulse.real)
#    plt.plot(pulse.imag)
#    plt.show()
    
    #Output file section.
    now = datetime.datetime.now()
    file_str = "OutputFiles/" + params.file + ".bin" #append the datetime to the end of the file.
    with open(file_str, 'wb') as file:
        file.write(bytearray(pulse))
        file.close()
    
quad_chirp()