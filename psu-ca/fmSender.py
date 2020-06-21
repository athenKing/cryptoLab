import requests
import json
from common.ds import genFlajoletMartin
from parameters import CONFIG
import random
from flask import Flask,request,jsonify
from ot.networkConfig import NETWORK

wLen =  CONFIG["DongLou"]["wLen"]
PRIME =  CONFIG["DongLou"]["PRIME"]
mLen =  CONFIG["DongLou"]["mLen"]

FS=None
PARTIALSUM =0
LASTR0=None

SENDER = Flask("fmSender")
@SENDER.route('/onInit',methods=['GET'])
def onInit():
	global FS,PARTIALSUM,PRIME,wLen,LASTR0

	fd = open('data/alice.data', 'r')
	alice = json.loads(fd.read())
	fd.close()

	FS = genFlajoletMartin(alice,wLen)
	PARTIALSUM = 0

    #Step 1:execuate OT(1,2) once
	r = random.randrange(1,PRIME)
	r0 = (PRIME-r)%PRIME
	r1= (PRIME-r+1)%PRIME

	PARTIALSUM += r
	LASTR0 = r0

	if FS[0] == '0':
		payload=json.dumps({'m0':str(r0),"m1":str(r1)})
	else:
		payload=json.dumps({'m0':str(r1),"m1":str(r1)})
	r = requests.post('http://0.0.0.0:{}/reset'.format(NETWORK["baseOTSender"]),json=payload)
	return "success"


#Step 2:execuate enough OT(1,4) several times
@SENDER.route('/onOthers',methods=['GET'])
def onOthers():
	global FS,PARTIALSUM,PRIME,wLen,LASTR0,mLen

	data = json.loads(request.get_json())
	curRound = data['round']

	r = random.randrange(1,PRIME)
	r0 = (PRIME-r)%PRIME
	r1= (PRIME-r+1)%PRIME

	PARTIALSUM+= r
	if FS[curRound]=='0':
		if LASTR0%2 == 0:
			messages = [r0,r0,r0,r1]
		else:
			messages = [r0,r1,r0,r0]
	else:
		if LASTR0%2 == 0:
			messages = [r0,r0,r1,r1]
		else:
			messages = [r1,r1,r0,r0]

	LASTR0 = r0
	payload={}
	payload["mLen"] = mLen
	payload["messages"] = messages
	payload["number"] = len(messages)
	r = requests.post('http://0.0.0.0:{}/onInit'.format(NETWORK["otExtSender"]),json=json.dumps(payload))
	return "success"

#Step 3:return this partial value to the other party
@SENDER.route('/onGetFinal',methods=['GET'])
def onGetFinal():
	global PARTIALSUM
	return jsonify({"partial":PARTIALSUM})

if __name__ == "__main__":
    SENDER.run(host='0.0.0.0',port=NETWORK["fmSender"])