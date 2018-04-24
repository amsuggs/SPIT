## Sim Pulsar 12ghz sampling -> downsample
# %matplotlib notebook
import numpy as np
import pickle
from matplotlib.pyplot import *

### gaussian pulse, 0.4ms width, 5ms period.  dm of 15? pc/cm^3. 0.15 second sim?
Fbw = 10e6  #total bandwidth wanted
Flo = 1.4e9 #Center frequency
fs_rf = 12e9 # Frequency running simulation at.


t = np.linspace(-0.0025,0.0025, 0.005*fs_rf) #create a time index, in seconds, 5ms total, center zero for ease.

# pulsar is basically a pulsed random noise signal.
l = len(t)
mu, sigma = 0, 1
s = np.random.normal(mu, sigma, l)  # create random noise signal

#turn random signal into pulsed.  
#gaussian profile  4ms width
s = np.exp(-t**2/(2*0.0004**2))*s

figure()
plot(s[::1000])

# freq data
fpulse = np.fft.fft(s)

# should look like nice broadband noise.  
freq = np.fft.fftfreq(l,1.0/(fs_rf/1e6))
figure()
plot(freq[::1000], np.abs(fpulse[::1000])**2)

#bandpass the pulse to receiver band.
Fbw = 10e6  #bandwidth wanted
Flo = 1.4e9 #Center frequency
fs_rf = 12e9 # Frequency running simulation at.
highpass_freq = Flo-Fbw/2.0
highpass_index1 = int(highpass_freq/(fs_rf/2)*l/2)
highpass_index2 = l - highpass_index1
fpulse[:highpass_index1] = 0
fpulse[highpass_index2:] = 0
nyquest_index = int(l/2)
lowpass_freq = Flo+Fbw/2.0
lowpass_index1 = int(lowpass_freq/(fs_rf/2)*l/2)
lowpass_index2 = l - lowpass_index1
fpulse[lowpass_index1:nyquest_index] = 0
fpulse[nyquest_index:lowpass_index2] = 0

freq = np.fft.fftfreq(l,1.0/(fs_rf/1e6))  #megahertz frequencies.
signal_lo_complex = np.exp(-2.0j*np.pi * Flo/fs_rf * np.arange(l) )  #create mixing signal

# now band limited,  Real signal.  
figure()
plot(freq[::1000], np.abs(fpulse[::1000])**2)

band_limited_s = np.fft.ifft(fpulse)

# show band limited pulse.  Still basically the same.  
figure()
plot(band_limited_s[::1000])

#mix down and filter, so that have I Q data for bandwidth
mixed_down_s = band_limited_s*signal_lo_complex
N_cutoff = int(Fbw/2/fs_rf*l)
fmixed = np.fft.fft(mixed_down_s)
fmixed[N_cutoff:-N_cutoff] = 0.0
filtered_mixed_down_s = np.fft.ifft(fmixed)
#Downsample so that is...
downsampled_filtered_mixed_down_s = filtered_mixed_down_s[::int(fs_rf/(Fbw))]
#complex sampled at 10MHz instead of 12GHz

# Any sim should basically be able to start here.  Use gaussian noise, filter with same time width.
figure()
plot(downsampled_filtered_mixed_down_s[::100].real)
plot(downsampled_filtered_mixed_down_s[::100].imag)

#repeat pulse to get ~0.15 sec.
downsampled_filtered_mixed_down_s_repeated = np.tile(downsampled_filtered_mixed_down_s, 30)

# Check how long dispersion actually is, need to have significantly longer than this worth of data to not worry.
#t_delay = 4.15e15 * (1/(1.2e9)**2 - 1/(1.6e9)**2) * 15
t_delay = 4.15e15 * (1/(1.395e9)**2 - 1/(1.405e9)**2) * 60
#const * (1/freq_low^2(Hz) - 1/(freq_high(Hz))^2) * DM #ans in s
print(t_delay)

#disperse:
#Create convolution in fourier space.
#this needs to be long relative to dispersion delay time.  
length = len(downsampled_filtered_mixed_down_s_repeated)
f = np.linspace(-Fbw/2,Fbw/2,length)
DM = 60
H =  np.exp(2j*np.pi*4.148808e15*DM*f**2/((Flo+f)*Flo**2))  #freq in Hz, +/- around flo

dispersed_downsampled_filtered_mixed_down_s = np.fft.ifft(np.fft.fft(downsampled_filtered_mixed_down_s_repeated)*H)

figure()
plot(dispersed_downsampled_filtered_mixed_down_s[::50].real)
plot(dispersed_downsampled_filtered_mixed_down_s[::50].imag)

##### Write to File #####
print("Start Writing...")
data_to_write = np.array([])
with open("k-pulse.bin", 'ab') as file:
    for index in range(0, dispersed_downsampled_filtered_mixed_down_s.size):
        imag = dispersed_downsampled_filtered_mixed_down_s[index].real
        real = dispersed_downsampled_filtered_mixed_down_s[index].imag
        p1 = -1 * real + 1j * imag
        file.write(bytes(np.complex64(p1)))
        tenth = dispersed_downsampled_filtered_mixed_down_s.size/10
        if((index % tenth) == 0):
            print(str(int(index / tenth * 10)) + "%")
        # data_to_write = np.append(data_to_write, np.complex64(p1))
    # file.write(bytearray(data_to_write))
print("Finished Writing")

#close('all')

#integrate to ~0.1ms, ~100khz resolution?
nfreq = 400
print(len(dispersed_downsampled_filtered_mixed_down_s)/nfreq)  #200 frequencies

#10msps complex
1/10e6

#want 0.2ms integrations
2e-4/(1/10e6)/nfreq

#integrate 5 samples
step = 400
int_size = 5
n_spectra = int(len(dispersed_downsampled_filtered_mixed_down_s)/step/int_size)
spec_out = np.zeros((n_spectra,step), dtype=complex)
for i in range(n_spectra):
    for j in range(int_size):
        #print(i,j)
        spec = np.fft.fft(dispersed_downsampled_filtered_mixed_down_s[(int_size*i+j)*step:(int_size*i+j+1)*step])
        spec_out[i] += spec*spec.conjugate()

spec_out.shape

figure()
plot(spec_out[:,399].real)
plot(spec_out[:,398].real)
plot(spec_out[:,300].real)

figure(figsize=(10,5))
imshow(spec_out.real)
# this is naturally top first time, bottom last time, lowest freq on left, highest on right.  
#  can see sweeping pulses starting top right, down to bottom left.

len(dispersed_downsampled_filtered_mixed_down_s)

dispersed_downsampled_filtered_mixed_down_s.dtype

dispersed_downsampled_filtered_mixed_down_s.real.max()

dispersed_downsampled_filtered_mixed_down_s.imag.max()

2**15-2

#dispersed_downsampled_filtered_mixed_down_s = dispersed_downsampled_filtered_mixed_down_s*32766/0.05556601286186533

#dispersed_downsampled_filtered_mixed_down_s.imag.max()

#dispersed_downsampled_filtered_mixed_down_s_real = dispersed_downsampled_filtered_mixed_down_s.real.astype(np.int16)
#dispersed_downsampled_filtered_mixed_down_s_imag = dispersed_downsampled_filtered_mixed_down_s.imag.astype(np.int16)

#dispersed_downsampled_filtered_mixed_down_s_real[:10]

#dispersed_downsampled_filtered_mixed_down_s.real[:10]

#dispersed_downsampled_filtered_mixed_down_s.real.max()

#dispersed_downsampled_filtered_mixed_down_s_real.shape

#out = np.zeros(2*len(dispersed_downsampled_filtered_mixed_down_s_real), dtype=np.int16)

#out[::2] = dispersed_downsampled_filtered_mixed_down_s_real
#out[1::2] = dispersed_downsampled_filtered_mixed_down_s_imag

#out[:20]

#out.shape

#out.tofile('pulse_sim_10mhz_int16_5ms_period_60dm_1400MHz_center_150ms_long.bin')

