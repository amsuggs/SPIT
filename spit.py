import numpy as np
import matplotlib.pyplot as plt
import math
import time
import spit_arg_parser as ap
import unit_exponent_parser as uep

vals = {}
params = ap.parse_args()
# Read in flags and arguments. Stored as dot-accessible members in a namespace.
# Used in the quad_chirp call at the end of the file using the parameters gathered from the argument parser.


# run all values through unit and exponent parser
def apply_units_and_exponentiation():
    vals['samples'] = int(uep.apply_unit_and_exponents(params.samples))
    vals['amplitude'] = float(uep.apply_unit_and_exponents(params.amplitude))
    vals['begin'] = int(uep.apply_unit_and_exponents(params.begin))
    vals['end'] = int(uep.apply_unit_and_exponents(params.end))
    vals['period'] = int(uep.apply_unit_and_exponents(params.period))
    if vals['period'] != params.period:
        vals['period'] *= 1000
    vals['offset'] = int(uep.apply_unit_and_exponents(params.offset))
    vals['peak'] = float(uep.apply_unit_and_exponents(params.peak))
    if vals['peak'] != params.peak:
        vals['peak'] *= 1000
    vals['width'] = float(uep.apply_unit_and_exponents(params.width))
    if vals['width'] != params.width:
        vals['width'] *= 1000
    
    print(vals)


apply_units_and_exponentiation()
# applies unit and exponent parsing


# Generates a quadratic chirp. Takes in number of samples, amplitude,
# starting frequency, ending frequency, sample time, and pulse offset.
# nr_samples should be twice the highest frequecy.
def quad_chirp(nr_samples=vals['samples'], amp=vals['amplitude'], f0=vals['begin'], f1=vals['end'], t1=vals['period'], phi=vals['offset']):
    print("nr_samples: %d, amp: %d, f0: %d, f1: %d, t1: %d, phi: %d" % (nr_samples, amp, f0, f1, t1, phi))
    # Calculation section.
    t1 = t1 / 1000
    t = np.linspace(0, t1, nr_samples)  # Array of samples.
    beta = (f1 - f0) / (t1 ** 2)  # Change between start and end frequencies.
    ft = f1 * t + beta * ((t1 - t) ** 3 - t1 ** 3) / 3  # Instantaneous frequency. Array.
    real = np.cos(2 * np.pi * ft + phi)  # Real component of the chirp.
    imag = np.sin(2 * np.pi * ft + phi)  # Imaginary component of the chirp.
    sig = amp * np.complex64(real - 1j * imag)  # Output signal. Real and imaginary components combined.
    
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


def gauss_pulse(chirp, x, mean=vals['peak'], std_dev=vals['width']):
    print("mean: %d, std_dev: %d" % (mean, std_dev))
    mean = mean / 1000
    std_dev = std_dev / 1000
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

    now = time.strftime("%m.%d.%Y") + "-" + time.strftime("%H.%M.%S")
    file_str = "OutputFiles/" + params.file + "(%s).bin" % now #append the datetime to the end of the file.
   
    with open(file_str, 'wb') as file:
        file.write(bytearray(pulse))
        file.close()


quad_chirp()
