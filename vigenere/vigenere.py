class VigenereAlgorithm(object):
	def __init__(self):
		self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		

	def getInverse(self,keys):
		inverse=''
		for i in keys:
			inverse+= chr(65 + (65+26-ord(i))%26) 
		return inverse

	def getMatrix(self,text,keyLen):
		matrix=[]
		#split into rows
		for row in range(keyLen):
			matrix.append([])
		for i in range(len(text)):
			mod = i%keyLen
			matrix[mod].append(text[i])
		return matrix

	def shiftText(self,text,offset):
		data = []
		for i in text:   #iterate over the text not some list
			if i.strip() and i in self.alpha: # if the char is not a space ""  
				data.append(self.alpha[(self.alpha.index(i) + offset) % 26])    
			else:
				data.append(i)
		output = ''.join(data)
		return output

	def mergeColoumns(self,matrix):
		#Merge the matrix into one plaintext
		text=''
		rows = len(matrix)
		for i in range(len(matrix[0])):
			for j in range(rows):
				if i == len(matrix[0])-1 and j>0 and len(matrix[j])<len(matrix[0]):
					break
				else:
					text+=matrix[j][i]

		lowercases=''
		for l in text:
			order = ord(l)
			if order >= 65 and order <= 90:
				lowercases+=chr(order+32)
			else:
				lowercases+=l

		return lowercases

	def encrypt(self,text,key):

		offset=[]
		for k in key:
			offset.append(ord(k)-65)

		matrix = self.getMatrix(text,len(offset))

		for i,v in enumerate(offset):
			matrix[i] = self.shiftText(matrix[i],v)

		# self.printInColum(matrix,ifKeyLen)
		# print("\n")
		return self.mergeColoumns(matrix)

	def decrypt(self,text,key,isEncryptKey):
		if not isEncryptKey:
			key = self.getInverse(key)

		return self.encrypt(text,key)



# def printInColum(self,matrix,ifKeyLen):
# 	print("\n............................")
# 	for row in range(ifKeyLen):
# 		listval = matrix[row]
# 		text=''
# 		for v in matrix[row]:
# 			text+=v
# 		print(text)
# 	print("............................\n")



# def printKey(self,keyArray):
# 	key=''
# 	for k in keyArray:
# 		key+=self.alpha[k]
# 	print("Final key is: ",key)