"""pulsar.py
module to create pulses
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import numpy as np
import scipy as sp
from scipy import stats
import h5py
import math
import time, sys
from . import PSS_utils as utils

class Pulsar(object):
    def __init__(self, Signal_in, period = 50, flux=3): #period in milliseconds
        """Intializes pulsar class. Inherits attributes of input signal class as well as pulse period.
        period = pulsar period in milliseconds.
        flux = mean flux density of pulsar in mJy
        Many other attributes can be set, including the statistical parameters of the pulse draws.
        """

        self.Signal_in = Signal_in
        self.signal = self.Signal_in.signal
        self.f0 = self.Signal_in.f0
        self.bw = self.Signal_in.bw
        self.Nf = self.Signal_in.Nf
        self.Nt = self.Signal_in.Nt
        self.Npols = self.Signal_in.Npols
        self.flux = flux
        self.SignalType = self.Signal_in.SignalType
        self.TotTime = self.Signal_in.TotTime
        self.TimeBinSize = self.Signal_in.TimeBinSize
        self.freqBinSize = self.Signal_in.freqBinSize
        self.T = period
        self.mode = self.Signal_in.MetaData.mode
        self.nBinsPeriod = int(self.T//self.TimeBinSize)
        self.NPeriods = np.int(self.TotTime//self.T) #Number of periods that can fit in the time given
        #self.time = np.linspace(0., self.TotTime, self.Nt)
        self.gamma_shape = 1
        self.gamma_scale = 2
        self.gauss_draw_sigma = 1
        self.phase = np.linspace(0., 1., self.nBinsPeriod)
        self.PulsarDict = dict(pulsar_period=period)
        self.PulsarDict['mean_flux'] = self.flux
        self.PulsarDict['signal_pulsed'] = False
        self.PulsarDict['nBins_per_period'] = self.nBinsPeriod
        self.NRows = self.Nf
        self.mem_size_limit = 100000
        if self.SignalType == 'voltage':
            self.NRows = int(4)
        self.gauss_template()

        if self.SignalType == 'voltage':
            gauss_limit = stats.norm.ppf(0.999, scale=self.gauss_draw_sigma)
            # Sets the limit so there is only a small amount of clipping because of dtype.
            self.gauss_draw_norm = self.Signal_in.MetaData.gauss_draw_max/gauss_limit
            # Normalizes the 99.9 percentile to the dtype maximum.

        elif self.SignalType == 'intensity':
            gamma_limit = stats.gamma.ppf(0.999, self.gamma_shape, scale=self.gamma_scale)
            # Sets the limit so there is only a small amount of clipping because of dtype.
            self.gamma_draw_norm = self.Signal_in.MetaData.gamma_draw_max/gamma_limit
            # Normalizes the 99.9 percentile to the dtype maximum.
        #TODO Add ability to deal with multiple bands
        #TODO Check to see that you have the correct kind of array and info you need


    def draw_intensity_pulse(self, reps):
        """draw_intensity_pulse(pulse)
        draw a single pulse as bin by bin random process (gamma distr) from input template
        shape and scale parameters can be set when Pulsar class intialized
        """
        pr = np.tile(self.profile, reps)
        L = pr.shape
        pulse = pr * self.gamma_draw_norm * np.random.gamma(self.gamma_shape, scale=self.gamma_scale, size=L)
        #pull from gamma distribution

        return pulse

    def draw_voltage_pulse(self, reps):
        """draw_voltage_pulse(pulse)
        draw a single pulse as bin by bin random process (normal distr) from input template
        """
        pr = np.tile(self.profile, reps)
        L = pr.shape
        pulse = pr * self.gauss_draw_norm * np.random.normal(0, self.gauss_draw_sigma, L) #pull from gaussian distribution

        return pulse

    def gauss_template(self, peak=0.25, width=0.05, amp=1.):
        """Sets the templates as gaussians or sums of gaussians.
        Assumed input describes the intensity profile.
        Each parameter input can either be a single float or an array of one of the following shapes:
            single float    : Single pulse profile made of a single gaussian
            1-d array       : Single pulse profile made up of multiple gaussians
            NRows x 1       : NRows of single gaussian profiles
            NRows x n       : NRows of multiple gaussian profiles
        where 'n' is the number of gaussians in a single profile.
        The first two options make a single profile which is tiled across the
        frequency bands (for an intensity signal). All inputs must be the same shape.
        If the same number of gaussians is not used in the last option,
        set trailing values as zero.

        peak = center of gaussian
        width = stdev of pulse
        amp = amplitude of pulse relative to other pulses.
        Pulses are normalized so that maximum is 1, for sampling reasons.
        See draw_voltage_pulse, draw_intensity_pulse and make_pulses() methods for more details.
        """
        #TODO: error checking for array length consistency?
        #TODO: if any param is a not array, then broadcast to all entries of other arrays?

        peak = np.array(peak)
        width = np.array(width)
        amp = np.array(amp)

        try:
            if peak.shape[0] == self.NRows :
                try: #Assumes peak.ndim = 2
                    if peak.shape[1] > 1: #Each Channel gets a different profile of multiple gaussians
                        self.PulsarDict["amplitude"] = amp
                        self.PulsarDict["Profile"] = "multiple gaussians"
                        self.profile = np.zeros((self.NRows,self.phase.size))
                        for jj in range(self.NRows):
                            amp[jj,:] = amp[jj,:]/amp[jj,:].max()  # normalize sum by row
                            row_profile = np.zeros(self.phase.size)
                            for ii in range(amp.shape[1]):
                                row_profile += amp[jj,ii] * np.exp(-0.5 * ((self.phase-peak[jj,ii])/width[jj,ii])**2)
                            row_profile /= row_profile.max() #Normalize sum
                            self.profile[jj,:] = row_profile
                    elif peak.shape[1] == 1: # Each channel gets a different profile made of one gaussian (array[[]])
                        self.profile = np.zeros((self.NRows,self.phase.size))
                        for jj in range(self.NRows):
                            self.profile[jj,:] = np.exp(-0.5 * ((self.phase-peak[jj,0])/width[jj,0])**2)
                            #NOTE: No amplitude, since only one amp get's normalized to one.
                        self.PulsarDict["amplitude"] = amp
                        self.PulsarDict["Profile"] = "gaussian"
                except: # Each channel gets a different profile made of one gaussian (array[])
                    # The case for peak_shape[0] = self.NRows and peak.ndim=1
                    self.profile = np.zeros((self.NRows, self.phase.size))
                    for jj in range(self.NRows):
                        self.profile[jj,:] = np.exp(-0.5 * ((self.phase-peak[jj])/width[jj])**2)
                    self.PulsarDict["amplitude"] = amp
                    self.PulsarDict["Profile"] = "gaussian"

            elif peak.shape[0] > 1 and peak.ndim == 1:
                self.PulsarDict["amplitude"] = amp
                self.PulsarDict["Profile"] = "multiple gaussians"

                row_profile = np.zeros(self.phase.size)
                self.profile = np.zeros((self.NRows, self.phase.size))
                for ii in range(amp.size):
                    self.profile += amp[ii] * np.exp(-0.5 * ((self.phase-peak[ii])/width[ii])**2)
                self.profile /= self.profile.max()  # normalize sum

            #elif peak.shape[0] and peak.ndim == 1:

            else:
                raise ValueError('Input arrays not of the correct shape. See documentation for details.')
        except:
            row_profile = np.exp(-0.5 * ((self.phase-peak)/width)**2)
            self.profile = np.tile(row_profile,(self.NRows,1))
            self.PulsarDict["amplitude"] = amp
            self.PulsarDict["Profile"] = "gaussian"

        self.PulsarDict["peak"] = peak
        self.PulsarDict["width"] = width
        if self.SignalType == 'voltage':
            self.profile = np.sqrt(self.profile)


    def user_template(self,template):
        """ Function to make any given 2-dimensional numpy array into the profile.
        Assumed to be the intensity profile.
        template is a numpy array. If larger than number of bins per period then downsampled.
        If smaller than number of bins per period then interpolated.
        """
        #TODO Allow other input files
        #TODO Adds error messages if not the correct type of file.
        self.PulsarDict["Profile"] = "user_defined"
        #TODO Add I/O for adding attributes for user defined templates.
        self.PulsarDict["peak"] = "None"
        self.PulsarDict["width"] = "None"
        self.PulsarDict["amplitude"] = "None"
        #self.nBinsPeriod = len(template)
        #self.profile = template
        try: # Assumes that template is a 1-d array and tiles it across a 2-d array: NRows x nBinsTemplate
            self.nBinsTemplate = template.size
            if self.nBinsTemplate==self.nBinsPeriod:
                self.profile = np.tile(template,(self.NRows,1)) #What

            elif self.nBinsTemplate > self.nBinsPeriod:
                #TODO Add in another elif to use down_sample() if an even divisor
                self.profile = np.tile(utils.rebin(template, self.nBinsPeriod),(self.NRows,1))
                print("User supplied template has been downsampled.")
                print("Input array length= ", self.nBinsTemplate,". Pulse template length= ",self.profile.shape[1],".")

            else:
                Len = template.shape[0]
                TempPhase = np.linspace(0, 1, Len)
                self.profile = np.zeros((self.NRows, self.nBinsPeriod))
                ProfileFcn = sp.interpolate.interp1d(TempPhase, template, kind='cubic', bounds_error=True)

                for ii in range(self.NRows):
                    self.profile[ii,:] = ProfileFcn(self.phase)
                print("User supplied template has been interpolated using a cubic spline.")
                print("Input array length was ", self.nBinsTemplate," bins. New pulse template length is ",self.profile.shape[1],".")

        except: # Exception assumes template is a 2-d array
            self.nBinsTemplate = template.shape[1]
            if self.nBinsTemplate==self.nBinsPeriod:
                self.profile = template

            elif self.nBinsTemplate > self.nBinsPeriod:
                #TODO Add in another elif to use down_sample() if an even divisor
                for ii in range(self.NRows):
                    self.profile[ii,:] = utils.rebin(template[ii,:], self.nBinsPeriod)
                print("User supplied template has been downsampled.")
                print("Input array length= ", self.nBinsTemplate,". Pulse template length= ",self.profile.shape[1],".")

            else:
                TempPhase = np.linspace(0,1,len(template))
                for ii in range(self.NRows):
                    ProfileFcn = sp.interpolate.interp1d(TempPhase, template[ii,:], kind='cubic', bounds_error=True)
                    self.profile[ii,:] = ProfileFcn(self.phase)
                print("User supplied template has been interpolated using a cubic spline.")
                print("Input array length was ", self.nBinsTemplate," bins. New pulse template length is ",self.profile.shape[1],".")
        self.MinCheck = np.amin(self.profile)
        if self.MinCheck < 0 :
            #Zeros out minimum intensity of profile, otherwise runs into problems
            #with positive-definite distributions for draws of pulses.
            self.profile = np.where(self.profile > 0, self.profile, self.profile-self.MinCheck)
            #TODO Message that you've shifted the array!
        
        self.profile /= self.profile.max()
        if self.SignalType == 'voltage':
            self.profile = np.sqrt(self.profile)


    def make_pulses(self, start_time = 0, stop_time = None):
        """Function that makes pulses using the defined profile template.
        Note: 'intensity'-type signals pulled from a gamma distribution using draw_intensity_pulse(),
            'voltage'-type signals pulled from a gaussian distribution using draw_voltage_pulse().
        """

        if self.PulsarDict['signal_pulsed']:
            raise ValueError('Signal has already been generated.')

        if stop_time == None:
            stop_time = self.TotTime
        start_bin = int(start_time // self.TimeBinSize )
        last_bin = int(stop_time // self.TimeBinSize )
        if stop_time == self.TotTime and start_time == 0:
            N_periods_to_make = self.NPeriods
            delta_bins = self.Nt
        elif stop_time < self.TotTime:
            delta_bins = last_bin - start_bin
            N_periods_to_make = int(delta_bins // self.nBinsPeriod)
        elif stop_time > self.TotTime:
            last_bin = self.Nt
            delta_bins = last_bin - start_bin
            N_periods_to_make = int(delta_bins // self.nBinsPeriod)
            #print('Stop time larger than total time. Stop time set to last time.')
        self.NLastPeriodBins = int(delta_bins % self.nBinsPeriod)#delta_bins - N_periods_to_make * self.nBinsPeriod #Length of last period
        pulseType = {"intensity":"draw_intensity_pulse", "voltage":"draw_voltage_pulse"}
        pulseTypeMethod = getattr(self, pulseType[self.SignalType])

        Nt_chunk = int(self.mem_size_limit // self.NRows)
        self.ChunkSize = int(Nt_chunk // self.nBinsPeriod) # Calc ChunkSize in integer number of periods


        if self.Nt * self.NRows > self.mem_size_limit and self.ChunkSize != 0 : #Limits the array size to 2.048 GB
            """The following limits the length of the arrays that we call from pulseTypeMethod(), by limiting the number
            of periods we pull from the distribution at one time. This is for machines with small amounts of memory, and
            is currently optimized for an 8GB RAM machine. In this process, most of the time is spent writing to disk.
            """

            self.Nchunks = int(N_periods_to_make // self.ChunkSize)
            self.NPeriodRemainder = int(N_periods_to_make % self.ChunkSize)
            pulse_start = time.time()

            for ii in range(self.Nchunks): #limits size of the array in memory
                self.signal[:, start_bin + ii * self.ChunkSize * self.nBinsPeriod : \
                            start_bin + (ii+1) * self.ChunkSize * self.nBinsPeriod] \
                            = pulseTypeMethod(self.ChunkSize)
                pulse_check = time.time()
                try: #Python 2 workaround. Python 2 __future__ does not have 'flush' kwarg.
                    print('\r{0}% sampled in {1:.2f} seconds.'.format((ii + 1)*100/self.Nchunks , pulse_check-pulse_start), end='', flush=True)
                except: #This is the Python 2 version.
                    print('\r{0}% sampled in {1:.2f} seconds.'.format((ii + 1)*100/self.Nchunks , pulse_check-pulse_start), end='')
                    sys.stdout.flush()

            if self.NPeriodRemainder != 0 :
                self.signal[:,start_bin + self.Nchunks * self.ChunkSize * self.nBinsPeriod : start_bin + (self.Nchunks * self.ChunkSize + self.NPeriodRemainder) * self.nBinsPeriod] = pulseTypeMethod(self.NPeriodRemainder)

        else:
            self.signal[:,start_bin:N_periods_to_make * self.nBinsPeriod] = pulseTypeMethod(N_periods_to_make) #Can be put into main flow for large RAM computers.

        self.LastPeriod = pulseTypeMethod(1)[:,0:self.NLastPeriodBins]
        self.signal[:,start_bin + N_periods_to_make * self.nBinsPeriod:start_bin + N_periods_to_make * self.nBinsPeriod + self.NLastPeriodBins] = self.LastPeriod

        self.PulsarDict['profile'] = self.profile
        self.PulsarDict['Smax'] = self.Smax
        if self.mode == 'explore':
            self.PulsarDict['signal_pulsed'] = True
        if self.SignalType == 'intensity':
            self.PulsarDict['gamma_draw_norm'] = self.gamma_draw_norm
            self.PulsarDict['gamma_shape'] = self.gamma_shape
            self.PulsarDict['gamma_scale'] = self.gamma_scale

        elif self.SignalType == 'voltage':
            self.PulsarDict['gauss_draw_norm'] = self.gauss_draw_norm
            self.PulsarDict['gauss_draw_sigma'] = self.gauss_draw_sigma

        self.Signal_in.MetaData.AddInfo(self.PulsarDict)

    @property
    def Smax(self):
        if not hasattr(self, '_Smax'):
            Smean = self.flux
            if self.SignalType == 'voltage':
                Smean = np.sqrt(Smean)
                norm = 1./self.Npols  # sum over polarizaitons
            else:
                norm = self.freqBinSize / self.bw  # sum over subbands

            pr = self.profile
            dph = self.phase[1] - self.phase[0]
            _Smax = Smean / (np.sum(pr) * dph * norm)

        return _Smax
