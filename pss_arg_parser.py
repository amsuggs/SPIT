#-h help
import argparse as ap

def parse_args():
    # Initialize ArgumentParser object.
    parser = ap.ArgumentParser(description = 'Generate Pulsar data.')

    # Add arguments to the parser.
    parser.add_argument('-r', '--frequency', help = 'Central frequency of the pulse.', default = 1400)
    parser.add_argument('-b', '--bandwidth', help = 'Bandwidth of the pulse.', default = 400)
    parser.add_argument('-p', '--period', help = 'Amount of time the sample will last, '
                        'measured in milliseconds.', default = 200)
    parser.add_argument('-f', '--file', help = 'Name for output file', default = 'pss_complex_pulse')
    parser.add_argument('-v', '--version', action = 'version', version = 'SPIT 0.1')
    parser.add_argument('-l', '--plot', action = 'store_true')
    
    # Parse the arguments as given by the command line.
    # Stores the results in a python namespace.
    args = parser.parse_args()

    return args
    # Access each element via dot notatio, e.g. print(args.bandwidth)
    # Example namespace: (bandwidth='1400', dispersion=81, frequency=400, output=None)