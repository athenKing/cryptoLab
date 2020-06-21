import requests
import json
from pybloom import BloomFilter
import numpy as np
import random
import math
from parameters import CONFIG
from ot.networkConfig import NETWORK


secureCoeffic = CONFIG["iknp"]["secureCoeffic"]
PRIME = CONFIG["iknp"]["PRIME"]
mLen = CONFIG["iknp"]["mLen"]
bfCapacity=CONFIG["bloomFilterCapacity"]


def npBool2Str(npBool):
	cur = ''
	for ele in npBool:
		cur += '1' if ele else '0'
	return cur

def generateBloom(data):
	bloom = BloomFilter(capacity=bfCapacity,error_rate=.001)
	for x in data:
		bloom.add(x)
	return bloom

def bitArray2npBool(bits):
	mLen = len(bits)
	ret = np.zeros(mLen,dtype = bool)
	for i in range(mLen):
		ret[i] = bits[i]
	return ret

def calcBloomSize(oneBits,num_bits,num_slices):
	base = 1-1/num_bits
	zeroBits = num_bits - oneBits
	return round(math.log(zeroBits/num_bits,base)/num_slices)


if __name__ == "__main__":
	##selection to be Bob's original mLen choice bits
	
	r = requests.get('http://0.0.0.0:{}/onInit'.format(NETWORK["aliceServer"]))


	fd = open('data/bob.data', 'r')
	bob = json.loads(fd.read())
	fd.close()
	bf = generateBloom(bob)


	bobSecrets = bitArray2npBool(bf.bitarray)
	mNumber = len(bobSecrets)

	# print("bob mNumber is: ",mNumber)
	secretStr = npBool2Str(bobSecrets)
	payload=json.dumps({'secureCoeffic':secureCoeffic,"mNumber":mNumber,"bobSecrets":secretStr,"mLen":mLen})

	r = requests.post('http://0.0.0.0:{}/onInit'.format(NETWORK["iknpBob"]),json=payload)

	print("Init aliceServer and iknpBob Successful!")
	'''
	TODO: Batch optimization
	'''
	for i in range(secureCoeffic):
		payload=json.dumps({'choiceRound':i})
		r = requests.get('http://0.0.0.0:{}/invokeBaseOT'.format(NETWORK["iknpBob"]),json=payload)


	union_partial=0

	result = None
	r = requests.get('http://0.0.0.0:{}/onRecovery'.format(NETWORK["iknpBob"]))
	result = r.json()['finalMsg']

	for e in result:
		union_partial+=int(e,2)

	r = requests.get('http://0.0.0.0:{}/onGetUnionPartionVal'.format(NETWORK["aliceServer"]))
	print("The final union value is: ",round(calcBloomSize((union_partial+r.json()['partial'])%PRIME,bf.num_bits,bf.num_slices)))
