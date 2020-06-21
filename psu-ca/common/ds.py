'''
It defines some datastructue
'''
from common.encode import int2bits
import hashlib

def genFlajoletMartin(data,w):
	hashfns=[hashlib.sha512,hashlib.sha384,hashlib.sha256,hashlib.sha1,hashlib.md5]
	for fn in hashfns:
		FS = ['0' for i in range(w)]
		hashfn = fn()
		for x in data:
			hashfn.update(int2bits(x))
			res = int(hashfn.hexdigest(),16)
			cnt = 0
			while res%2 !=1:
				cnt+=1
				res >>= 1
			FS[cnt]='1'
		break
	return FS



# def genFlajoletMartin(data):
# 	w = 15
# 	hashfns=[hashlib.sha512,hashlib.sha384,hashlib.sha256,hashlib.sha1,hashlib.md5]

# 	m=len(hashfns)
# 	z=0
# 	for fn in hashfns:
# 		FS = ['0' for i in range(w)]
# 		hashfn = fn()
# 		for x in data:
# 			hashfn.update(int2bits(x))
# 			res = int(hashfn.hexdigest(),16)
# 			cnt = 0
# 			while res%2 !=1:
# 				cnt+=1
# 				res >>= 1
# 			FS[cnt]='1'
# 		# return FS
# 		for v in FS:
# 			if v != '0':
# 				z+=1
# 			else:
# 				break
# 	# z+=1
# 	z/=m
# 	return (FS,round((2**z)/.77351))