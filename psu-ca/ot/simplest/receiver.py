
import requests
import hashlib,random,json
from gmpy2 import powmod

P=(1<<607) - 1
G = 17

def hashFunc(int_val):
	h = hashlib.sha256()
	h.update(str(int_val).encode('utf-8'))
	return int(h.hexdigest(),16)

def int2bits(x):
	x=int(x)

	length = len(str(hex(x)))-2
	if length%2 == 1:
		length+=1
	length//=2

	bits = x.to_bytes(length,byteorder="big")
	return bits


class SimplestReceiver:
	def __init__(self):
		self.Kc = 0
		self.B = 0
		pass

	def initiate(self,choice):
		global G,P

		try:
			r = requests.get('http://0.0.0.0:8080/1stRequest')
		except:
			print("why request encounters exception?")

		A = int((r.json())['A'])
		b = random.randrange(1,P)
		B = powmod(G,b,P)
		if choice:
			B = (A*B)%P

		self.B = B
		self.Kc = hashFunc(int(powmod(A,b,P)))

	def final(self):
		payload=json.dumps({'B':int(self.B)})
		try:
			r = requests.get('http://0.0.0.0:8080/2stRequest',data=payload)
		except:
			print("why request encounters exception?")

		e0 = (r.json())['e0']
		e1 = (r.json())['e1']

		m0 = e0 ^ self.Kc
		m1 = e1 ^ self.Kc

		try:
			m = int2bits(m0).decode('utf-8')
			return m[6:]
		except UnicodeDecodeError:
			pass

		try:
			m = int2bits(m1).decode('utf-8')
			return m[6:]
		except UnicodeDecodeError:
			pass


if __name__ == "__main__":
    recv = SimplestReceiver()
    recv.initiate(0)
    recv.final()