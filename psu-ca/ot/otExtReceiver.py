import requests
import json
from flask import request
from ot.simplest.receiver import SimplestReceiver
from ot.networkConfig import NETWORK

class GeneralOTReceiver:
	def __init__(self,choice):
		self.choice = choice

		self.simplestRecv = SimplestReceiver()

		r = requests.get('http://0.0.0.0:{}/onGetEncrypted'.format(NETWORK["otExtSender"]))
		data = r.json()

		self.encrypted = data['encrypted']
		self.choiceKeys = []

		for i,b in enumerate(self.choice):
			self.initiate(i,int(b))



	def initiate(self,curRound,choice):
		r = requests.get('http://0.0.0.0:{}/onSelect'.format(NETWORK["otExtSender"]),json=json.dumps({"round":curRound}))

		self.simplestRecv.initiate(choice)

		self.choiceKeys.append(int(self.simplestRecv.final()))


	def final(self):

		decrypt = self.encrypted[int(self.choice,2)]

		for v in self.choiceKeys:

			decrypt ^= v

		return decrypt