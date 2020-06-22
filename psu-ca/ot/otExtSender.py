'''
It implements a 1/n OT
input: (M0,M1,M2,...,M_(n-1)) choice:c

Call order
'''
from flask import Flask,request,jsonify
import requests
import json
import math

from networkConfig import NETWORK


def int2str(intLen,Integer):
	modulo = 1<<intLen
	Integer = Integer % modulo
	text = '0'*intLen
	Integer = bin(Integer)[2:]
	final = text[:intLen-len(Integer)] + Integer
	return final

def genKeyPairs(length,keyLen):
	import random
	right =  (1<<length) -1
	left = 1<<(length -1)
	pairs=[]
	for i in range(keyLen):
		pair = []
		for j in range(2):
			pair.append(random.randrange(left,right))
		pairs.append(pair)
	return pairs

messages=None
keyPairs=None
encrypted=None
# M0 M1 SHOULD BE A STRING CONTAINS ONLY 0 OR 1

SENDER = Flask("OTExtSender")

@SENDER.route('/onInit',methods=['POST'])
def onInit():
	global messages,keyPairs,encrypted

	data = json.loads(request.get_json())
	messages = data['messages']
	mLen = data['mLen']
	number = data['number']

	keyLen = math.ceil(math.log(number,2))

	keyPairs = genKeyPairs(mLen,keyLen)

	# print(keyPairs)
	encrypted=[]
	for i,m in enumerate(messages):
		bits = int2str(keyLen,i)
		enc = m
		for j,b in enumerate(bits):
			enc ^= keyPairs[j][int(b)]
		encrypted.append(enc)

	return "Success"


@SENDER.route('/onGetEncrypted',methods=['GET'])
def onGetEncrypted():
	global encrypted
	return jsonify({'encrypted':encrypted})

 
@SENDER.route('/onSelect')
def onSelect():
	global keyPairs

	data = json.loads(request.get_json())
	curRound = data['round']

	payload=json.dumps({'m0':str(keyPairs[curRound][0]),"m1":str(keyPairs[curRound][1])})

	r = requests.post('http://0.0.0.0:{}/reset'.format(NETWORK["baseOTSender"]),json=payload)

	return "Success"


if __name__ == "__main__":
    SENDER.run(host='0.0.0.0',port=NETWORK["otExtSender"])