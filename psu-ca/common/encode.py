
def int2bits(x):
	x=int(x)

	length = len(str(hex(x)))-2
	if length%2 == 1:
		length+=1
	length//=2

	bits = x.to_bytes(length,byteorder="big")
	return bits

def bits2int(bits):
	return int.from_bytes(bits,byteorder="big")