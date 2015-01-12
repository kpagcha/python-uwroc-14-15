import random

def rand_perm(L):
	L = L[:]
	random.shuffle(L)
	return L

def randperm(L):
	L = L[:]
	result = []
	while L:
		position = random.randint(0, len(L)-1)
		result.append(L[position])
		del L[position]
	return result

L = [1,2,3,4,5,6,7,8,9,0]
print randperm(L)