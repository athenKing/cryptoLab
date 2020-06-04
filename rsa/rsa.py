import os
import hashlib
from random import randrange
from primes import generate_large_prime, gcd, extended_gcd, is_prime
from encode import int2bits,bits2int
from gmpy2 import powmod

CONSTANT_PK=31

class RSA:
	def __init__(self):
		self.pk = CONSTANT_PK
		self.params = dict()

	def keygen(self,keySize):
		p = generate_large_prime(keySize)
		# print("p is: ",p)
		q = generate_large_prime(keySize)
		# print("\nq is: ",q)
		N = p*q
		euler_N = (p-1)*(q-1)
		sk = extended_gcd(euler_N,self.pk)[2]
		if sk < 0:
			sk+=euler_N
		self.params['pk']=self.pk
		self.params['sk']=sk
		self.params['N']=N
		return self.params

	def prepareBinary(self,binary):
		ret = int(hashlib.sha256(binary).hexdigest(),16)
		return ret % self.params['N']

	def encrypt(self,binary):
		num = self.prepareBinary(binary)
		return powmod(num,self.params['pk'],self.params['N'])

	def decrypt(self,cipher):
		return powmod(cipher, self.params['sk'], self.params['N'])

	'''
	return binary signatue
	'''
	def sign(self,binary):
		num = self.prepareBinary(binary)
		num = self.decrypt(num)
		return int2bits(num)

	def verify(self,binary,signature):
		val = bits2int(signature)
		return powmod(val, self.params['pk'], self.params['N']) == self.prepareBinary(binary)

if __name__ == '__main__':
	rsa = RSA()
	rsa.keygen(512)

	with open("encode.py", 'rb') as binary_file:
		data = binary_file.read()
		signature = rsa.sign(data)
		print(rsa.verify(data,signature))
		
		print(signature)
		fw = open('signature.bin','wb')
		fw.write(signature)
		fw.close()
    