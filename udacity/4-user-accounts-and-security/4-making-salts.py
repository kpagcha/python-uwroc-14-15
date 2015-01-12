import random
import string

# implement the function make_salt() that returns a string of 5 random
# letters use python's random module.
# Note: The string package might be useful here.

def make_salt():
    r = ""
    for i in xrange(0, 5):
        r += random.choice(string.ascii_letters)
    return r

print make_salt()