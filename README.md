# SPIT 0.1
**S**ynthetic **P**ulsar for **I**nstrument **T**esting

## Dependencies
* numpy
* scipy
* matplotlib

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
4. pulsar file will be out putted into hte PulsarSignalOutputs directory


## Developer Information
SPIT's first implementation relied heavily on the Pulsar Signal Simulator (PSS) library, but has since moved on to implementations developed by the SPIT team themselves. PSS may be integrated and supported in future versions.

## Flags

* -n: Number of samples for given time period, default = 8192
* -a: Amplitude of sine/cosine, default = 1.0
* -b: Beginning frequency, deafult = 20
* -e: Ending frequency, default = 0
* -t: Amount of time the sample will last in seconds, deafult = 1
* -p: Phase offset, default = 0.0
* -o: Name of the output file, default = "spit_pulse"
* -v: Version, SPIT 0.1


