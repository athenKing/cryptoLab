import random
import math
import bitarray
import numpy as np
import json
from bloom.pybloom import BloomFilter



def generateBloom(data):
	bloom = BloomFilter(capacity=10,error_rate=.1)
	for x in data:
		bloom.add(x)
	return bloom

def unionBinStr(a,b):
	intersect = 0
	for i in range(len(a)):
		if a[i] == '1' and b[i] == '1':
			intersect+=1

	return intersect

def getDATA(filepath):
	fd = open(filepath, 'r')
	val = json.loads(fd.read())
	fd.close()
	return val

def getBitStr(filepath):
	fd = open(filepath, 'r')
	val = json.loads(fd.read())
	fd.close()
	bf = generateBloom(val)
	ret = ''
	for e in bf.getBits():
		if e:
			ret += '1'
		else:
			ret += '0'

	return ret

def estimateBloomSize(bf):
	zeroBits = bf.bitarray.count(False)
	per = bf.bits_per_slice
	return -per*(math.log(zeroBits/bf.num_bits))


def showBasicInfo(bf):
	print("Number of Filter Bits:", bf.num_bits)
	print("Number of slices:", bf.num_slices)
	print("Bits per slice:", bf.bits_per_slice)

	oneBits = bf.bitarray.count(True)
	zeroBits = bf.bitarray.count(False)
	print ("Number of 1 bits:", oneBits)
	print ("Number of 0 bits:", zeroBits)


	for i in range(bf.num_slices):
		print("BitArray is like: ",bf.bitarray[i*bf.bits_per_slice:(i+1)*bf.bits_per_slice])
	# print("BitArray is like: ",bf.bitarray[:11])



val1 = []
limit = 5
for i in range(limit):
	val1.append(i)
bf1 = generateBloom(val1)
showBasicInfo(bf1)






val2 = []
limit = 5
for i in range(limit,2*limit):
	val2.append(i)
bf2 = generateBloom(val2)
showBasicInfo(bf2)



estimateBloomSize


# errorCnt=0
# StartX=9000
# rangeLen = 10000
# for i in range(StartX,StartX+rangeLen):
# 	if i in bf1:
# 		errorCnt+=1
# print("false positive rate is: ",errorCnt/rangeLen)


print("estimation of bf1 is: ",estimateBloomSize(bf1))
print("estimation of bf2 is: ",estimateBloomSize(bf2))

print("estimation of union is: ",estimateBloomSize(bf1.union(bf2)))
print("estimation of intersection is: ",estimateBloomSize(bf1.intersection(bf2)))






