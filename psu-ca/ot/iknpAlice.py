import random
import json
import numpy as np
from simplest.receiver import SimplestReceiver
import requests
import hashlib
from flask import Flask,jsonify,request


'''
Below four functions are encoding decoding functions
'''
def npBool2Str(npBool):
	cur = ''
	for ele in npBool:
		cur += '1' if ele else '0'
	return cur

def str2npBool(strVal):
	strLen = len(strVal)
	ret = np.zeros(strLen,dtype = bool)
	for index,val in enumerate(strVal):
		if val == '1':
			ret[index] = True
	return ret

def bigInt2npBool(intLen,bigInt):
	modulo = 1<<intLen
	bigInt = bigInt % modulo
	text = '0'*intLen
	binInt = bin(bigInt)[2:]
	final = text[:intLen-len(binInt)] + binInt
	return str2npBool(final)

def npBool2BigInt(npBool):
	strVal = npBool2Str(npBool)
	return int(strVal,2)

'''
Oracle Funciton: [m] x {0,1}^{lambda} -> {0,1}^l
'''
def hashFunc(mLen,j,npBoolArray,finalLen):
	outLen = len(bin(mLen)) - 2

	h = hashlib.sha256()

	initial = '0'*outLen

	binJ = bin(j)[2:]

	middle = initial[:outLen-len(binJ)] + binJ

	final = middle + npBool2Str(npBoolArray)
	h.update(final.encode('utf-8'))
	return bigInt2npBool(finalLen,int(h.hexdigest(),16))


'''
secureCoeffic: secure parameter defines the security strength
mNumber: round number of the messages
messages: mNumber pairs of messages with mLen length
mLen: every single message length
'''
class iknpAlice:
	def __init__(self,secureCoeffic,mNumber,messages,mLen):
		self.secureCoeffic = secureCoeffic
		self.mNumber = mNumber
		self.messages = messages
		self.mLen = mLen

		self.secrets = np.empty(secureCoeffic,dtype = bool)
		for i in range(secureCoeffic):
			self.secrets[i] = random.randrange(0,2) == 1

		self.Q = np.empty([mNumber,secureCoeffic],dtype = bool)

	def getRandomSecret(self):
		return self.secrets

	# Q = np.empty([mNumber,secureCoeffic],dtype = bool)
	def setMatrixQ(self,index,strVal):
		self.Q[:,index] = str2npBool(strVal)
		return  (index == self.secureCoeffic-1)
	
	# messages = np.empty([mNumber,2,mLen],dtype = bool)
	def prepareMsgForBob(self):
		Y = self.messages.copy()
		Ystr = []

		for i in range(self.mNumber):
			Y[i,0,:] = self.messages[i,0,:] ^ hashFunc(self.mNumber,i,self.Q[i,:],self.mLen)
			Y[i,1,:] = self.messages[i,1,:] ^ hashFunc(self.mNumber,i,self.Q[i,:] ^ self.secrets,self.mLen)

			Ystr.append([npBool2Str(Y[i,0,:]),npBool2Str(Y[i,1,:])])

		return Ystr



ikAlice = None
simplestRecv = SimplestReceiver()


iknpAliceEntity = Flask("IKNPAlice")
@iknpAliceEntity.route('/onInit',methods=['POST'])
def onInit():
	global ikAlice

	data = json.loads(request.get_json())

	secureCoeffic = data['secureCoeffic']
	mNumber = data['mNumber']
	messages = data['messages']
	mLen = data['mLen']

	nBoolMessages = np.empty([mNumber,2,mLen],dtype = bool)
	for i in range(mNumber):
		nBoolMessages[i,0,:] = str2npBool(messages[i][0])
		nBoolMessages[i,1,:] = str2npBool(messages[i][1])

	ikAlice  = iknpAlice(secureCoeffic,mNumber,nBoolMessages,mLen)

	return "InitSuccess"



@iknpAliceEntity.route('/evokeChoice',methods=['GET'])
def evokeChoice():
	global simplestRecv,ikAlice

	data = json.loads(request.get_json())

	curRound = data['choiceRound']

	secret = ikAlice.getRandomSecret()

	simplestRecv.initiate(secret[curRound])

	isFinished = ikAlice.setMatrixQ(curRound,simplestRecv.final())

	if isFinished:
		Ystr = ikAlice.prepareMsgForBob()

		payload=json.dumps({'matrixY':Ystr})

		try:
			r = requests.post('http://0.0.0.0:9001/onSetBobMatrix',json=payload)
		except:
			print("why request encounters exception?")

		return "FINISHED"


	return "UNFINISHED"


if __name__ == "__main__":
    iknpAliceEntity.run(host='0.0.0.0',port=9000)


	
