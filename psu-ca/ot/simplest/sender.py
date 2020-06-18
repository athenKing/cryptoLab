'''
It implements a 1/2 OT
input: (M0,M1) choice:c

Call order
'''
from flask import Flask,jsonify,request
import hashlib,random
from gmpy2 import powmod
# from common.encode import bits2int
# import requests
import json
import ast


# import logging
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
def bits2int(bits):
	return int.from_bytes(bits,byteorder="big")

def enc(key,message):
	key = int(key)
	h = hashlib.sha256()
	h.update(str(key).encode('utf-8'))
	hashKey = int(h.hexdigest(),16)


	m = bytes("prefix"+message,"utf-8")
	m = bits2int(m)

	# m = int(message,2)

	cipher = hashKey ^ m
	return cipher


P=(1<<607) - 1
G = 17
a,A = 0,0

M0,M1="alice","bob"

# M0 M1 SHOULD BE A STRING CONTAINS ONLY 0 OR 1

SENDER = Flask("OTSender")

@SENDER.route('/reset',methods=['POST'])
def reset():
	global M0,M1

	data = json.loads(request.get_json())
	M0 = data['m0']
	M1 = data['m1']
	return "Success"


@SENDER.route('/1stRequest')
def onStart():
    global P,a,A
    a = random.randrange(1,P)
    A = int(powmod(G,a,P))
    return jsonify({'A':A})

@SENDER.route('/2stRequest',methods=['GET'])
def onEnc():
	global P,a,MO,M1,A

	data = ast.literal_eval((request.data).decode('utf-8'))
	B = int(data['B'])
	e0 = enc(powmod(B,a,P),M0)
	base = powmod(A,-1,P)
	base = powmod(B*base,a,P)
	e1 = enc(base,M1)
	return jsonify({'e0':e0,'e1':e1})


if __name__ == "__main__":
    #Start the sender
    SENDER.run(host='0.0.0.0',port=8080)