import random
import math
import bitarray
import numpy as np
import json
from bloom.pybloom import BloomFilter



def generateBloom(data):
	bloom = BloomFilter(capacity=5000,error_rate=.01)
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

def intersectionOfLists(list1,list2):
	intersection = []
	for a in list1:
		if a in list2:
			intersection.append(a)
	return intersection



def estimateBloomSize(bf):
	zeroBits = bf.bitarray.count(False)
	per = bf.bits_per_slice
	return -per*(math.log(zeroBits/bf.num_bits))

def estimateBloomSize2(bf):
	zeroBits = bf.bitarray.count(False)
	base = 1-1/bf.num_bits
	return round(math.log(zeroBits/bf.num_bits,base)/bf.num_slices)


def showBasicInfo(bf):
	print("Number of Filter Bits:", bf.num_bits)
	print("Number of slices:", bf.num_slices)
	print("Bits per slice:", bf.bits_per_slice)

	oneBits = bf.bitarray.count(True)
	zeroBits = bf.bitarray.count(False)
	print ("Number of 1 bits:", oneBits)
	print ("Number of 0 bits:", zeroBits)

def zeroFormu(bf,a):
	return bf.num_bits*(1-1/bf.num_bits)**(bf.num_slices*a)

def oneFormu(bf,a):
	return bf.num_bits-bf.num_bits*(1-1/bf.num_bits)**(bf.num_slices*a)

def intersectFormu(m,k,a,b):
	base = 1-1/m
	p1 = base**(k*a)
	p2 = base**(k*b)
	p = p1+p2 - p1*p2
	# print("aaa ",b**(k*a))
	# print("aaa ",b**(k*a))
	return m*p

def doubleCheckIntersect(bfIntersect,valList):
	cnt=0
	for v in valList:
		if v in bfIntersect:
			cnt +=1
	return cnt

fd = open('data/alice.data', 'r')
alice = json.loads(fd.read())
fd.close()
bf1 = generateBloom(alice)

showBasicInfo(bf1)

fd = open('data/bob.data', 'r')
bob = json.loads(fd.read())
fd.close()
bf2 = generateBloom(bob)

bf = bf1.union(bf2)

showBasicInfo(bf)

aliceEstimate = estimateBloomSize2(bf1)
bobEstimate = estimateBloomSize2(bf2)

print("alice estimate is: ",aliceEstimate)
print("bob estimate is: ",bobEstimate)


unionEstimate = estimateBloomSize2(bf)
print("union estimate is: ",unionEstimate)

bfInter = bf1.intersection(bf2)
print("experimental intersect estimate is: ",estimateBloomSize2(bfInter)," vs ",aliceEstimate+bobEstimate-unionEstimate)



print(doubleCheckIntersect(bfInter,alice))
print(doubleCheckIntersect(bf2,alice))

# print("theory zerobits of intersection is: ",intersectFormu(bf.num_bits,bf.num_slices,len(alice),len(bob))," vs ",bf2.intersection(bf1).bitarray.count(False))

# intersection = intersectionOfLists(alice,bob)
# bf3 = generateBloom(intersection)
# print("direct estimate is: ",estimateBloomSize2(bf3))


# print("zero estimate is: ",zeroFormu(bf2,len(bob))," vs ",bf2.bitarray.count(False))
# print("one estimate is: ",oneFormu(bf2,len(bob))," vs ",bf2.bitarray.count(True))

'''
Original message:
Alice len is:  783
Bob len is:  3026
Union value is:  3407
Intersection value is:  402


Original bloom filter message:
781.4768976536911 vs 783
3028.8369711722453 vs 3026

onebits cnt is:  27181

3414.5043295563355 vs 3407

395.8095392696009 vs 402


Final OT-based bloom filter message:

'''





