from bloom.pybloom import BloomFilter
from common.encode import int2bits
import pickle
import hashlib

from ot.fmsender import startSender
from ot.fmReceiver import startReceiver

# b1 = BloomFilter(capacity=len(alice)*5,error_rate=.00001)

# for x in alice:
# 	b1.add(x)

# for x in alice:
# 	print(x in b1)

# print(1 in b1)

# print(len(b1))
def genFlajoletMartin(data):
	'''
	using sha256 as random bits generator
	'''
	w = 256
	FS = ['0' for i in range(w)]

	sha256 = hashlib.sha256()
	for x in data:
		sha256.update(int2bits(x))
		res = int(sha256.hexdigest(),16)
		cnt = 0
		while res%2 !=1:
			cnt+=1
			res >>= 1
		FS[cnt]='1'

	return FS
	# z=0
	# while FS[i] != '0':
	# 	z+=1
	# return z

if __name__ == "__main__":
	inputFile = 'data/alice.data'
	fd = open('data/alice.data', 'rb')
	alice = pickle.load(fd)
	fm1 = genFlajoletMartin(alice)
	fd.close()
	startSender(fm1)

	fd = open('data/bob.data', 'rb')
	bob = pickle.load(fd)
	fm2 = genFlajoletMartin(bob)
	fd.close()
	startReceiver(fm2)

	
	

	



