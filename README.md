# SPIT 0.1
**S**ynthetic **P**ulsar for **I**nstrument **T**esting

## Dependencies
* python
* numpy
* scipy
* matplotlib
* Jupyter Notebooks --Optional

## Getting Started

1. Install python<br>
    https://www.python.org/downloads/
2. Get python dependencies<br>
    https://www.anaconda.com/download/
3. Install jupyter notebook (optional)<br>
    http://jupyter.org/install

## Run In Terminal

1. clone this repository
2. cd into root directory of the repository
3. `python spit.py`
4. pulsar file will be out putted into hte OutpuFile directory

## Flags

* -s, --samples: Number of samples in given time period, default = 8192
* -a, --amplitude: Amplitude of cosine/sine wave, default = 1.0
* -b, --begin: Beginning frequency, frequency sweep will begin at this value, measured in Hz., default = 20
* -e, --end: Ending frequency, Frequency sweep will end at this value, measured in Hz, default = 0
* -p, --period: Amount of time the cycle will last, measured in seconds, default = 1
* -o, --offset: Phase offset, default = 0.0
* -f, --file: Name for output file, default = 'spit_pulse'
* -k, --peak: Where the peak of the pulse occurs in the period, measured in milliseconds, default = 500
* -w, --width: The width of the pulse, measured in milliseconds, default = 100

For the begin, end, and width flags the frequency values can be with or without units. spit.py supports YHz, ZHz, EHz, PHz, THz, GHz, MHz, kHz, hHz, DHz, dHz, cHz, mHz, uHz, nHz, pHz, fHz, aHz, zHz, yHz. **WARNING MHz and larger unit types take up a lot of memory.**


## Developer Information
SPIT's first implementation relied heavily on the Pulsar Signal Simulator (PSS) library, but has since moved on to implementations developed by the SPIT team themselves. PSS may be integrated and supported in future versions.

### GNU Radio
We used GNU Radio to test the pulses. To get started with GNU Radio https://gnuradio.org/

### Creating Pulses
To create our pulse we create a frequency sweep from the starting frequency and ending at the end frequency. The generated sweep is then put over a normal distribution using a Gaussian function. Currently the created pulse as a dispersion that is locked in to be align with the period.

### File Writing
spit.py currently writes in an interleaving real and imaginaryy flaot32 format e.g. (1.0 1.0j 1.0 1.0j ...). This is to allow for testing with GNU radio. For details on how to read these files using GNU Radio refer back to the GNU Radio section above.

### Other Files
There currently exist two other files in this repository to create a pulse pss.py and pulsar_simulator_10mhz.py. pss.py is using a library called PSS https://github.com/Hazboun6/VersionZeroPointZero also generates pulsar pulses, the PSS repository is currently awaiting major refactor. Looking into this might be good in the future.

pulsar_simulator_10mhz.py creates a pulse that has its signal attributes hardcoded. This is intented to show an example of dispersion that goes beyond the period of the pulse. This file can be used as a start off point for future development.


