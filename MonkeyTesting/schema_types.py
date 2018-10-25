import random

#int
def negative_int(range=4000000):
    return random.randint(1, range) * (-1)

def return_zero():
    return 0

def positive_int(range=4000000):
    return random.randint(1, range)

intf = [negative_int, return_zero, positive_int]

#float
def negative_float(range=8000000):
    return random.randint(1, range) * (-1)

def positive_float(range=8000000):
    return random.randint(1, range)

floatf = [negative_float, return_zero, positive_float]

#bool
boolf = [True, False]

#str
def ascii_str(size=30):
    ascii_string = ''
    for i in range(0, size + 1):
        ascii_string += chr(random.randint(32, 128))
    return ascii_string

def unicode(size=30):
    unicode_string = ''
    for i in range(0, size + 1):
        unicode_string += chr(random.randint(32, 1000))
    return unicode_string

def return_empty_str():
    return ''

def return_False():
    return False

def return_True():
    return True
strf = [return_zero, ascii_str, unicode]

types = {'int': intf, 'str': strf, 'float': floatf, 'bool': [True, False]}
enum_of_types = {int: intf, str: strf, float: floatf, bool: [return_True, return_False]}