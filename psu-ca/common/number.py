import gmpy2
import math
from itertools import count
import random

smallprimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
           43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
           101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
           151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
           199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
           263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
           317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
           383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
           443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
           503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
           577, 587, 593, 599, 601, 607, 613, 617, 619, 631,
           641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
           701, 709, 719, 727, 733, 739, 743, 751, 757, 761,
           769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
           839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
           911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
           983, 991, 997, 1009, 1013, 1019, 1021, 1031, 1033,
           1039, 1049, 1051, 1061, 1063, 1069, 1087, 1091, 1093,
           1097, 1103, 1109, 1117, 1123, 1129, 1151, 1153, 1163,
           1171, 1181, 1187, 1193, 1201, 1213, 1217, 1223, 1229]
"""
Miller Rabin prime test
"""
def is_prime(n):
	s=0
	d=n-1
	while d%2==0:
		d=d>>1
		s+=1
	t=40
	n_bits = 1 + int(math.log(n, 2))
	for k, tt in ((100, 27), (150, 18),(200, 15),(250, 12),(300, 9),(350, 8),(400, 7),(450, 6),(550, 5),(650, 4), (850, 3),(1300, 2),):
		if n_bits < k:
			break
		t=tt

	for i in range(t):
		a=smallprimes[i]
		y = gmpy2.powmod(a,d,n)
		if y!=1 and y!=n-1:
			j=1
			while j<=s-1:
				y=gmpy2.powmod(y,2,n)
				if y==n-1:
					break
				j+=1
			if j == s:
				return False
	return True

'''
Using Polland's rho original rand number generating function
Combining Brent's cycle detection
Optimization on reducing gcd operations
This method is only applicable for rsa cracking with smaller factors
'''
def pollardRoh(n):
	x = 2
	for cycle in count(1):
		y = x
		for i in range(2**cycle):
			x = (x*x + 1) % n
			factor = gcd(x-y, n)
			if factor > 1:
				return factor

def pollardRoh1(n):
	x = 2
	z=1
	for cycle in count(1):
		y = x
		iterations = 2**cycle
		for i in range(iterations):
			x = (x*x + 1) % n
			z=(z*abs(y-x))%n
			if i%127==0 or i==iterations-1:
				factor = gcd(z, n)
				if factor > 1:
					return factor

#There're several ways solving the problem fastly
def factorization(n):
	pollardRoh1(n)
		

def gcd(a, b):
    """Greatest common divisor using Euclid's algorithm."""
    while a:
        a, b = b % a, a
    return b

def gen_prime(keysize):
	while True:
		num = random.randrange( 1<<(keysize-1),1<<keysize )
		if is_prime(num):
			return num

if 3 & 1:
	print(is_prime(65531))



