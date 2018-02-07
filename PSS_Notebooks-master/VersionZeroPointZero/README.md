# Pulsar Signal Simulator Version 0.0

This document serves as a summary of the __Pulsar Signal Simulator Working Group__’s plan for the first version of the simulator.
In our first two meetings it was decided that the simulator will be written using ```Python 3.x``` (including imports from the ```__future__``` module for ```Python 2.7``` compatibility) and that a private GitHub page will be used for storing and collaborating on the code.
If you wish to have access to the GitHub repository please contact Nathaniel Garver-Daniels and include you GitHub username and he will send you an invitation.

## The Signal

The main structure of the code will consist of a signal which will be a class object.
It will be acted on by other classes modeling the physical processes a pulsar signal experiences as it propagates.
The signal class will consist of time series data, modeling the pulsar signal and acted upon by other classes, and metadata containing the past history of the time series and chronicling the physical processes the time series has passed through.
In an effort to obtain a minimal working model as efficiently as possible the first version of the signal will be a single series of intensity versus time data with a sampling frequency about ten times that of a telescopes sampling frequency.
The signal will be designed, from the beginning, with the goal of expanding the number of time series and increasing the sampling frequency.

## The Modules

The modules will each be class objects that model various physical processes acting on the signal.
They will take the signal class as their primary input along with any other necessary parameters needed to model the physical process.
Each module will model the various changes to the pulsar signal and will add any information to the metadata of the signal class needed to understand the history of those processes.

Inputs for modules will be function calls whenever possible, however the ability to input ```.par``` files will be built in so that known pulsars can be modeled without need for reentering known data.
The final output should be a format that can be readily used by existing analysis, such as ```.fits```.
The minimal working version of the simulator will consist of a Pulsar Module, an ISM Module and a Telescope module.
The pulses will be formed from modulating a white noise background using a gaussian pulse shape.
The module will be designed with the goal of generalizing the input pulse shape and allowing for multiple bands and bandwidths.
Other modules that have been discussed include, but are not limited to:
* Binary Module
* Gravitational Wave Module
* Ephemeris Module
* Ionospheric Module
* Interplanetary Module
* Telescope Backend Module
