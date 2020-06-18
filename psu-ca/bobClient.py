import requests
import json
from bloom.pybloom import BloomFilter

from parameters import CONFIG
secureCoeffic = CONFIG["iknp"]["secureCoeffic"]
PRIME = CONFIG["iknp"]["PRIME"]
mLen = CONFIG["iknp"]["mLen"]

bfCapacity=CONFIG["bloomFilterCapacity"]



import numpy as np
import random

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


if __name__ == "__main__":
	##selection to be Bob's original mLen choice bits
	
	try:
		r = requests.get(CONFIG["networkPort"]["aliceServer"]+'onInit')
	except:
		print("Init networkPort::aliceServer onInit Error!")


	fd = open('data/bob.data', 'r')
	bob = json.loads(fd.read())
	fd.close()
	bf = generateBloom(bob)

	bobSizeEstimate = calcBloomSize(bf.bitarray.count(True),bf.num_bits,bf.num_slices)


	bobSecrets = bitArray2npBool(bf.getBits())
	mNumber = len(bobSecrets)

	# print("bob mNumber is: ",mNumber)

	secretStr = npBool2Str(bobSecrets)
	payload=json.dumps({'secureCoeffic':secureCoeffic,"mNumber":mNumber,"bobSecrets":secretStr,"mLen":mLen})

	try:
		r = requests.post(CONFIG["networkPort"]["iknpBob"]+'onInit',json=payload)
	except:
		print("Init networkPort::aliceServer onInit Error!")


	'''
	TODO: Batch optimization
	'''
	for i in range(secureCoeffic):
		payload=json.dumps({'choiceRound':i})
		try:
			r = requests.get(CONFIG["networkPort"]["iknpBob"]+'invokeBaseOT',json=payload)
			# print(r.text)
		except:
			print("why request encounters exception?")




	union_partial=0
	intersection_partial =bobSizeEstimate

	result = None
	try:
		r = requests.get(CONFIG["networkPort"]["iknpBob"]+'onRecovery')
		result = r.json()['finalMsg']
	except:
		print("why request encounters exception?")

	for e in result:
		union_partial+=int(e,2)

	intersection_partial-=union_partial
	if intersection_partial<0:
		intersection_partial = PRIME - intersection_partial

	print(intersection_partial)


	try:
		r = requests.get(CONFIG["networkPort"]["aliceServer"]+'onGetUnionPartionVal')
		print("The final union value is: ",round(calcBloomSize((union_partial+r.json()['partial'])%PRIME,bf.num_bits,bf.num_slices)))
	except:
		print("why request encounters exception?")


	# try:
	# r = requests.get(CONFIG["networkPort"]["aliceServer"]+'onGetIntersectionPartionVal')
	# val = (intersection_partial+r.json()['partial'])%PRIME
	# print(val)
	# val = math.ceil(val)
	# print(val)
	# print("The final intersection value is: ",calcBloomSize(val,bf.num_bits,bf.num_slices))
	# except:
		# print("why request encounters exception?")





	


