
import random
import json
import numpy as np
from simplest.receiver import SimplestReceiver
import requests
import hashlib

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
Input parameters

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
		self.secretChoices = secretChoices

		#Generating a random matrix firstly
		self.T = np.empty([mNumber,secureCoeffic],dtype = bool)
		for i in range(mNumber):
			for j in range(secureCoeffic):
				self.T[i][j] = (random.randrange(0,2) == 1)

		#M is the message to be send
		self.M = np.empty([secureCoeffic,2,mNumber],dtype = bool)

		for i in range(secureCoeffic):
			self.M[i,0,:] = self.T[:,i]
			self.M[i,1,:] = secretChoices ^ self.T[:,i]

	def genMessageByRound(self,curRound):
		payload=json.dumps({'m0':npBool2Str(self.M[curRound,0,:]),"m1":npBool2Str(self.M[curRound,1,:])})
		try:
			r = requests.post('http://0.0.0.0:8080/reset',json=payload)
		except:
			print("Unknown Error!!")

	# Y = np.empty([mNumber,2,mLen],dtype = bool)
	def recoveryOriginalMsg(self,Y):
		Z = np.empty([self.mNumber,self.mLen],dtype = bool)
		for i in range(self.mNumber):
			cur = 1 if self.secretChoices[i] else 0
			Z[i,:] = Y[i,cur,:] ^ hashFunc(self.mNumber,i,self.T[i,:],self.mLen)
		return Z


class iknpAlice:
	def __init__(self,secureCoeffic,mNumber,messages,mLen):
		self.secureCoeffic = secureCoeffic
		self.mNumber = mNumber
		self.messages = messages
		self.mLen = mLen

		self.secrets = np.empty(secureCoeffic,dtype = bool)
		for i in range(secureCoeffic):
			self.secrets[i] = random.randrange(0,2) == 1

	def getRandomSecrets(self):
		return self.secrets

	# Q = np.empty([mNumber,secureCoeffic],dtype = bool)
	# messages = np.empty([mNumber,2,mLen],dtype = bool)
	def prepareMsgForBob(self,Q):
		Y = self.messages.copy()
		for i in range(self.mNumber):
			Y[i,0,:] = self.messages[i,0,:] ^ hashFunc(self.mNumber,i,Q[i,:],self.mLen)
			Y[i,1,:] = self.messages[i,1,:] ^ hashFunc(self.mNumber,i,Q[i,:] ^ self.secrets,self.mLen)
		return Y


# def startSender():


# seperate alice and bob in network configuration
if __name__ == "__main__":
	secureCoeffic = 50
	mNumber=20
	P = (1<<521) - 1
	mLen = 521

	##selection to be Bob's original mLen choice bits
	bobSecrets = np.empty(mNumber,dtype = bool)
	for j in range(mNumber):
		bobSecrets[j] = (random.randrange(0,2) == 1)
	ikBob = iknpBob(secureCoeffic,mNumber,mLen,bobSecrets)

	
	# alice = np.empty(mNumber,dtype = bool)
	# for j in range(mNumber):
	# 	alice[j] = (random.randrange(0,2) == 1)
	# ##the standard message pair input of Alice
	# messages = np.empty([mNumber,2,mLen],dtype = bool)
	# Z1 = 0
	# for j in range(mNumber):
	# 	r = random.randrange(1,P) 
	# 	pairs=[]
	# 	if alice[j]:
	# 		val = bigInt2npBool(mLen,(P-r+1)%P)
	# 		messages[j,0,:] = val
	# 		messages[j,1,:] = val
	# 	else:
	# 		messages[j,0,:] = bigInt2npBool(mLen,P-r)
	# 		messages[j,1,:] = bigInt2npBool(mLen,(P-r+1)%P)
	# 	Z1 += r




	#Alice generate random secret and using it to get partial info of Bob's random matrix 
	ikAlice  = iknpAlice(secureCoeffic,mNumber,messages,mLen)
	aliceRandomSecret = ikAlice.getRandomSecrets()
	Q = np.empty([mNumber,secureCoeffic],dtype = bool)
	simplestRecv = SimplestReceiver()
	for i in range(secureCoeffic):
		ikBob.genMessageByRound(i)
		simplestRecv.initiate(aliceRandomSecret[i])
		Q[:,i] = str2npBool(simplestRecv.final())



	#send messages to Bob
	bobGet = ikAlice.prepareMsgForBob(Q)

	
	finalMsg = ikBob.recoveryOriginalMsg(bobGet)


	Z2 = 0
	for j in range(mNumber):
		Z2 += npBool2BigInt(finalMsg[j])

	print( (Z1+Z2)%P )

	print(npBool2Str(bobSecrets))
	print(npBool2Str(alice))


	# testing of correctness-1
	# direct = np.empty([mNumber,mLen],dtype = bool)
	# for i in range(mNumber):
	# 	cur = 1 if bobSecrets[i] else 0
	# 	direct[i,:] = messages[i,cur,:]
	# a = npBool2Str(direct[10,:])


	# b = npBool2Str(finalMsg[10,:])
	# print(a == b)





	












	














