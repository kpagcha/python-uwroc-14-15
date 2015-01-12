import math

def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_happy(n):
	count = 0
	while n != 0:
		if n%10 == 7:
			count += 1
			if count == 3:
				return True
		else:
			count = 0
		n /= 10
	return count == 3

for i in range(777, 1000000):
	if is_happy(i) and is_prime(i):
		print i