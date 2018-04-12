#-h help
import argparse as ap

def parse_args():
    #Initialize ArgumentParser object.
    parser = ap.ArgumentParser(description = 'Generate Pulsar data.')

    #Add arguments to the parser.
    parser.add_argument('-s', '--samples', help = 'Number of samples in given time period', default = 8192)
    parser.add_argument('-a', '--amplitude', help = 'Amplitude of cosine/sine wave.', default = 1.0)
    parser.add_argument('-b', '--begin', help = 'Beginning frequency, '
                        'Frequency sweep will begin at this value, '
                        'measured in Hz.', default = 20)
    parser.add_argument('-e', '--end', help = 'Ending frequency, '
                        'Frequency sweep will end at this value, ' 
                        'measured in Hz.', default = 0)
                        # TODO change to Period in ms
    parser.add_argument('-p', '--period', help = 'Amount of time the sample will last, '
                        'measured in milliseconds.', default = 1000)
    parser.add_argument('-o', '--offset', help = 'Phase offset', default = 0.0)
    parser.add_argument('-f', '--file', help = 'Name for output file', default = 'spit_pulse')
    parser.add_argument('-k', '--peak', help = 'Where the peak of the pulse occurs in the period, '
                        'measured in milliseconds', default = 500)
    parser.add_argument('-w', '--width', help = 'The width of the pulse, '
                        'measured in milliseconds', default = 100)
    parser.add_argument('-v', '--version', action = 'version', version = 'SPIT 0.1')

    #Parse the arguments as given by the command line.
    #Stores the results in a python namespace.
    args = parser.parse_args()

    return args
    #Access each element via dot notatio, e.g. print(args.bandwidth)
    #Example namespace: (bandwidth='1400', dispersion=81, frequency=400, output=None)
