
import random
import json
import numpy as np
import requests
import hashlib
from flask import Flask,jsonify,request

from networkConfig import NETWORK

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
mLen: every single message length in binary
secretChoice: bob's secret choices in every OT round
'''
class iknpBob:
	def __init__(self,secureCoeffic,mNumber,mLen,secretChoices):
		self.secureCoeffic = secureCoeffic
		self.mNumber = mNumber
		self.mLen = mLen

		#the length of secretChoices the same as mNumber
		self.secretChoices = str2npBool(secretChoices)

		#Generating a random matrix firstly
		self.T = np.empty([mNumber,secureCoeffic],dtype = bool)
		for i in range(mNumber):
			for j in range(secureCoeffic):
				self.T[i][j] = (random.randrange(0,2) == 1)

		#M is the message to be send
		self.M = np.empty([secureCoeffic,2,mNumber],dtype = bool)

		for i in range(secureCoeffic):
			self.M[i,0,:] = self.T[:,i]
			self.M[i,1,:] = self.secretChoices ^ self.T[:,i]

	def genMessageByRound(self,curRound):
		payload=json.dumps({'m0':npBool2Str(self.M[curRound,0,:]),"m1":npBool2Str(self.M[curRound,1,:])})
		try:
			r = requests.post('http://0.0.0.0:{}/reset'.format(NETWORK["baseOTSender"]),json=payload)
		except:
			print("Unknown Error!!")

	def setMatrixY(self,Ystr):
		self.matrixY = np.empty([self.mNumber,2,self.mLen],dtype = bool)
		for i in range(self.mNumber):
			self.matrixY[i,0,:] = str2npBool(Ystr[i][0])
			self.matrixY[i,1,:] = str2npBool(Ystr[i][1])


	def recoveryOriginalMsg(self):
		# finalMsg = np.empty([self.mNumber,self.mLen],dtype = bool)
		finalMsg = []
		for i in range(self.mNumber):
			cur = 1 if self.secretChoices[i] else 0
			# finalMsg[i,:] = self.matrixY[i,cur,:] ^ hashFunc(self.mNumber,i,self.T[i,:],self.mLen)
			finalMsg.append(npBool2Str(self.matrixY[i,cur,:] ^ hashFunc(self.mNumber,i,self.T[i,:],self.mLen)))
		# ret = []
		return finalMsg



ikBob = None
iknpBobEntity = Flask("IKNPBob")
@iknpBobEntity.route('/onInit',methods=['POST'])
def onInit():
	global ikBob

	data = json.loads(request.get_json())

	secureCoeffic = data['secureCoeffic']
	mNumber = data['mNumber']
	bobSecrets = data['bobSecrets']
	mLen = data['mLen']

	ikBob = iknpBob(secureCoeffic,mNumber,mLen,bobSecrets)

	return "onInit iknpBobEntity Success!"


@iknpBobEntity.route('/invokeBaseOT',methods=['GET'])
def invokeBaseOT():
	global ikBob

	data = json.loads(request.get_json())

	curRound = data['choiceRound']

	ikBob.genMessageByRound(curRound)

	#After message reset,bob envoke alice to choose a secret bit here
	payload=json.dumps({'choiceRound':curRound})
	try:
		r = requests.get('http://0.0.0.0:{}/evokeChoice'.format(NETWORK["iknpAlice"]),json=payload)
	except:
		print("why request encounters exception?")

	return r.text



@iknpBobEntity.route('/onSetBobMatrix',methods=['POST'])
def onSetBobMatrix():
	global ikBob

	data = json.loads(request.get_json())
	matrixY = data['matrixY']

	ikBob.setMatrixY(matrixY)

	return "Success"


@iknpBobEntity.route('/onRecovery',methods=['GET'])
def onRecovery():
	global ikBob
	
	finalMsg = ikBob.recoveryOriginalMsg()
	return jsonify({"finalMsg":finalMsg})

	
# seperate alice and bob in network configuration
if __name__ == "__main__":
	iknpBobEntity.run(host='0.0.0.0',port=NETWORK["iknpBob"])