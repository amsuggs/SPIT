#-b bandwith(in MHz) -f frequency(in MHz) -p period(in ms)? -d dispersion(in ?)
#-h help
import argparse as ap

#Initialize ArgumentParser object.
parser = ap.ArgumentParser(description = 'Generate Pulsar data.')

#Add arguments to the parser.
parser.add_argument('-b', '--bandwidth', help = 'specify bandwidth, '
                    'measured in MHz', default = 1400)
parser.add_argument('-f', '--frequency', help = 'specify frequency, '
                    'measured in MHz', default = 400)
parser.add_argument('-d', '--dispersion', help = 'specify dispersion, '
                    'measured in magic?', default = 81)

parser.add_argument('output', nargs = '?', help = 'name for output file')
parser.add_argument('-v', '--version', action = 'version', version = 'SPIT 0.1')

#Parse the arguments as given by the command line.
#Stores the results in a python namespace.
args = parser.parse_args()

#Access each element via dot notatio, e.g. print(args.bandwidth)
#Example namespace: (bandwidth='1400', dispersion=81, frequency=400, output=None)
