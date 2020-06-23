'''
It implements a 1/n OT
input: (M0,M1,M2,...,M_(n-1)) choice:c
'''
from flask import Flask,request,jsonify
import requests
import json
import math
import hashlib
from networkConfig import NETWORK


from fastecdsa import keys,curve
from fastecdsa.encoding.pem import PEMEncoder


sk = None
S=None
T=None
N=None


SENDER = Flask("OTEcSender")
@SENDER.route('/onInit',methods=['POST'])
def onInit():
	global sk,M,S,T

	data = json.loads(request.get_json())
	M = data["messages"]

	sk,S = keys.gen_keypair(curve.P256)
	T = sk*S
	return "success"


@SENDER.route('/onGetPk',methods=['GET'])
def onGetPk():
	global S

	return jsonify({"S":PEMEncoder.encode_public_key(S)})


@SENDER.route('/onReceiveR',methods=['POST'])
def onReceiveR():
	global S,T,sk,M

	data = json.loads(request.get_json())
	R = PEMEncoder.decode_public_key(data["R"], curve.P256)

	cipher=[]
	
	for j in range(len(M)):
		P = (sk*R)-(j*T)

		combine = str(S)+str(8*R)+str(64*P)
		hfunc = hashlib.sha3_256(combine.encode('utf-8'))
		k = hfunc.hexdigest()
		k1 = int(k[:32],16)
		k2 = int(k[32:],16)

		enc = [M[j]^k1,k2]
		cipher.append(enc)

	return jsonify({"cipher":cipher})


if __name__ == "__main__":
    SENDER.run(host='0.0.0.0',port=NETWORK["otEcSender"])