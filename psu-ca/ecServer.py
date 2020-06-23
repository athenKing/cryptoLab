import requests
import json
from pybloom import BloomFilter
import numpy as np
import random
import math
from parameters import CONFIG
from ot.networkConfig import NETWORK


if __name__ == "__main__":
	upper = (1<<128) -1
	N = 10
	M=[]
	for i in range(N):
		m = random.randrange(1,upper)
		M.append(m)

	print(M)

	data=json.dumps({"messages":M})
	r = requests.post('http://0.0.0.0:{}/onInit'.format(NETWORK["otEcSender"]),json=data)