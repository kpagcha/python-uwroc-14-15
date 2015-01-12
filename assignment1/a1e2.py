import math

def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    sqrt = math.sqrt(n)
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def generate():
    happy_list = []

    for i in xrange(0, 10):
        for j in xrange(0, 10):
            for k in xrange(0, 10):
                happy_list.append(int(str(i) + str(j) + str(k) + '7777777'))
                happy_list.append(int(str(i) + str(j) + '7777777' + str(k)))
                happy_list.append(int(str(i) + '7777777' + str(j) + str(k)))
                happy_list.append(int('7777777' + str(i) + str(j) + str(k)))

    return sorted(happy_list)
    
some_super_happy_numbers = generate()

for i in some_super_happy_numbers:
    if is_prime(i):
        print i