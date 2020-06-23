import requests
import json
import random
import hashlib
from ot.networkConfig import NETWORK

from fastecdsa import keys,curve
from fastecdsa.encoding.pem import PEMEncoder


if __name__ == "__main__":
	x,PK = keys.gen_keypair(curve.P256)


	r = requests.get('http://0.0.0.0:{}/onGetPk'.format(NETWORK["otEcSender"]))
	S = PEMEncoder.decode_public_key(r.json()["S"], curve.P256)


	choice = random.randrange(0,10)
	R=S*choice + PK
	P = x*S
	hfunc = hashlib.sha3_256()
	combine = str(S)+str(8*R)+str(64*P)
	hfunc.update(combine.encode('utf-8'))
	k = hfunc.hexdigest()
	k1 = int(k[:32],16)
	k2 = int(k[32:],16)

	data = json.dumps({"R":PEMEncoder.encode_public_key(R)})
	r = requests.post('http://0.0.0.0:{}/onReceiveR'.format(NETWORK["otEcSender"]),json=data)
	cipher = r.json()["cipher"]

	plainNumber = 0
	for c in cipher:
		if c[1] == k2:
			plainNumber = c[0] ^ k1
			break

	print("Choice is {}, final number is {} ".format(choice,plainNumber))


