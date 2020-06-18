
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
			self.M[i,1,:] = secretChoices ^ self.T[:,i]

	def genMessageByRound(self,curRound):
		payload=json.dumps({'m0':npBool2Str(self.M[curRound,0,:]),"m1":npBool2Str(self.M[curRound,1,:])})
		try:
			r = requests.post('http://0.0.0.0:8080/reset',json=payload)
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
		return  (index == self.secureCoeffic)
	
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




@iknpAliceEntity.route('/envokeChoice',methods=['POST'])
def evokeChoice():
	global simplestRecv,ikAlice

	data = json.loads(request.get_json())
	curRound = data['choiceRound']

	secret = ikAlice.getRandomSecret()

	simplestRecv.initiate(aliceRandomSecret[curRound])

	isFinished = ikAlice.setMatrixQ(curRound,simplestRecv.final())

	if isFinished:
		Ystr = ikAlice.prepareMsgForBob()

		payload=json.dumps({'matrixY':Ystr})
		try:
			r = requests.post('http://0.0.0.0:9001/onSetBobMatrix',json=payload)
		except:
			print("why request encounters exception?")


	return jsonify({"finished":isFinished})





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

	for i in range(secureCoeffic):
		ikBob.genMessageByRound(i)

		#After message reset,bob envoke alice to choose a secret bit here
		payload=json.dumps({'choiceRound':i})
		try:
			r = requests.post('http://0.0.0.0:9000/evokeChoice',json=payload)
		except:
			print("why request encounters exception?")

	return "onInit iknpBobEntity Success!"

@iknpBobEntity.route('/onSetMatrix',methods=['POST'])
def onSetBobMatrix():
	global ikBob

	data = json.loads(request.get_json())
	matrixY = data['matrixY']
	ikBob.setMatrixY(matrixY)


@iknpBobEntity.route('/onRecovery',methods=['GET'])
def onRecovery():
	global ikBob
	
	finalMsg = ikBob.recoveryOriginalMsg()
	return jsonify({"finalMsg":finalMsg})

	





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

	
	alice = np.empty(mNumber,dtype = bool)
	for j in range(mNumber):
		alice[j] = (random.randrange(0,2) == 1)
	##the standard message pair input of Alice
	messages = np.empty([mNumber,2,mLen],dtype = bool)
	Z1 = 0
	for j in range(mNumber):
		r = random.randrange(1,P) 
		pairs=[]
		if alice[j]:
			val = bigInt2npBool(mLen,(P-r+1)%P)
			messages[j,0,:] = val
			messages[j,1,:] = val
		else:
			messages[j,0,:] = bigInt2npBool(mLen,P-r)
			messages[j,1,:] = bigInt2npBool(mLen,(P-r+1)%P)
		Z1 += r




	#Alice generate random secret and using it to get partial info of Bob's random matrix

	ikAlice  = iknpAlice(secureCoeffic,mNumber,messages,mLen)#belong to outside caller
	aliceRandomSecret = ikAlice.getRandomSecret()#belong to outside caller


	Q = np.empty([mNumber,secureCoeffic],dtype = bool)#belong to AliceEntity

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





	












	














