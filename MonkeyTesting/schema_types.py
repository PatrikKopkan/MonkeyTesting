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

#str
def ascii_str(size=30):
    ascii_string = ''
    for _ in range(0, size + 1):
        ascii_string += chr(random.randint(32, 128))
    return ascii_string

def unicode_text(size=30):
    unicode_string = ''
    for _ in range(0, size + 1):
        unicode_string += chr(random.randint(32, 1000))
    return unicode_string

def return_empty_str():
    return ''
    
def back_slashes(size=30):
    return '\b' * size

strf = [ascii_str, unicode_text, return_empty_str, return_zero, back_slashes]
#bool
def return_False():
    return False

def return_True():
    return True
boolf = [return_True, return_False]

enum_of_types = {int: intf, str: strf, float: floatf, bool: boolf}