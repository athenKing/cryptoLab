import requests
import json
import math
import numpy as np
import random
from parameters import CONFIG
from bloom.pybloom import BloomFilter
from flask import Flask,request


secureCoeffic = CONFIG["iknp"]["secureCoeffic"]
PRIME = CONFIG["iknp"]["PRIME"]
mLen = CONFIG["iknp"]["mLen"]


bfCapacity=CONFIG["bloomFilterCapacity"]


def bigInt2binStr(mLen,val):
	initial = '0'*mLen
	binStr = bin(val)[2:]
	return initial[:mLen-len(binStr)] + binStr

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

def calcBloomSize(one_Bits,num_bits,num_slices):
	import math
	return -num_bits/num_slices*(math.log(1-one_Bits/num_bits))

union_partial=0
intersection_partial =0

aliceServer = Flask("aliceServer")
@aliceServer.route('/onInit',methods=['GET'])
def onInit():
	global union_partial

	fd = open('data/alice.data', 'r')
	alice = json.loads(fd.read())
	fd.close()
	bf = generateBloom(alice)

	aliceSizeEstimate = calcBloomSize(bf.bitarray.count(True),bf.num_bits,bf.num_slices)


	alice = bitArray2npBool(bf.getBits())
	mNumber = len(alice)

	# print("alice mNumber is: ",mNumber)

	messages = []
	for j in range(mNumber):
		r = random.randrange(1,PRIME) 
		pairs=[]
		if alice[j]:
			val = bigInt2binStr(mLen,(PRIME-r+1)%PRIME)
			pairs.append(val)
			pairs.append(val)
		else:
			pairs.append(bigInt2binStr(mLen,PRIME-r))
			pairs.append(bigInt2binStr(mLen,(PRIME-r+1)%PRIME))
		union_partial += r
		messages.append(pairs)

	oneBits = bf.bitarray.count(True)

	intersection_partial = aliceSizeEstimate - union_partial
	if intersection_partial<0:
		intersection_partial = PRIME - intersection_partial

	# print(intersection_partial)
	# print("alice secret is: ",npBool2Str(alice))
	# print("Z1 is: ",Z1)

	payload=json.dumps({'secureCoeffic':secureCoeffic,"mNumber":mNumber,"messages":messages,"mLen":mLen})
	try:
		r = requests.post(CONFIG["networkPort"]["iknpAlice"]+'onInit',json=payload)
	except:
		print("why request encounters exception?")

	return r.text

@aliceServer.route('/onGetUnionPartionVal',methods=['GET'])
def onGetUnionPartionVal():
	global union_partial
	return json.dumps({'partial':union_partial})


# @aliceServer.route('/onGetIntersectionPartionVal',methods=['GET'])
# def onGetIntersectionPartionVal():
# 	global intersection_partial
# 	return json.dumps({'partial':intersection_partial})
	
'''
Input:  Prepared messages
Output: None
'''
if __name__ == "__main__":
	aliceServer.run(host='0.0.0.0',port=9002)