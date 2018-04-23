import re

prefix_map = {}


# fills dictionary with common metric prefixes with their corresponding exponentiation
def define_prefix_map():
    if 'Y' in prefix_map:
        return
    prefix_map['Y'] = 24
    prefix_map['Z'] = 21
    prefix_map['E'] = 18
    prefix_map['P'] = 15
    prefix_map['T'] = 12
    prefix_map['G'] = 9
    prefix_map['M'] = 6
    prefix_map['k'] = 3
    prefix_map['h'] = 2
    prefix_map['D'] = 1
    prefix_map['d'] = -1
    prefix_map['c'] = -2
    prefix_map['m'] = -3
    prefix_map['u'] = -6
    prefix_map['n'] = -9
    prefix_map['p'] = -12
    prefix_map['f'] = -15
    prefix_map['a'] = -18
    prefix_map['z'] = -21
    prefix_map['y'] = -24


# gets exponentiation for unit prefix
def get_exp(prefix):
    return prefix_map[prefix]


# checks to see format of input string
# accepts formats:
#           5e-9  --exponentiation
#           5nm   --prefix + unit
#           5n    --only prefix
def apply_unit_and_exponents(inputStr):
    define_prefix_map()
    # if not string
    if not isinstance(inputStr, str):
        return inputStr

    modified_str = inputStr.replace(' ', '')
    modified_str = modified_str.replace('+', '')

    matcher = re.compile('(-?\d+[.]?\d*)e(-?\d+)([a-zA-Z])(?:[a-zA-Z]?)*');
    matches = matcher.match(modified_str)
    if matches:
        retval = float(matches.group(1)) * (pow(10.0, float(matches.group(2))))

        exponent = get_exp(matches.group(3))
        if not exponent:
            raise ValueError('Invalid Prefix: ' + matches.group(3))
        return float(retval * (pow(10.0, exponent)))

    # regular expression to match "digits"e"optional-""digits"
    # ex: 5e-20
    matcher = re.compile('(-?\d+[.]?\d*)e(-?\d+)')
    matches = matcher.match(modified_str)
    if matches:
        return float(matches.group(1)) * (pow(10.0, float(matches.group(2))))

    # regular expression matching number
    matcher = re.compile('(-?\d+[.]?\d*)([a-zA-Z])(?:[a-zA-Z]?)*')
    matches = matcher.match(modified_str)
    # if unit...ed?
    if matches:
        exponent = get_exp(matches.group(2))
        if not exponent:
            raise ValueError('Invalid Prefix: ' + matches.group(2))
        return float(matches.group(1)) * (pow(10.0, exponent))

    return inputStr

