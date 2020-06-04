

class Frequency(object):
	def __init__(self,container=None):

		self.container = []

		if container and len(container) == 26:
			self.container = container
		else:
			for i in range(26):
				self.container.append(0)

	def put(self,index,val):
		self.container[index]= val

	def shift(self,offset):
		temp = self.container[offset:] + self.container[:offset]
		self.container = temp
		return self

	def countDiff(self,other):
		assert type(other) is Frequency,"compared value must be Frequency type"
		diff = 0
		for i in range(26):
			diff += abs(self.container[i]-other.container[i])

		return diff

	def countDiff1(self,other):
		assert type(other) is Frequency,"compared value must be Frequency type"
		diff = 0
		for i in range(26):
			diff += self.container[i]*other.container[i]

		return diff


	def __add__(self, other):
		if not isinstance(other, Frequency):
			return NotImplemented

		newFreq = Frequency()
		for i in range(26):
			newFreq.container[i] = self.container[i] + other.container[i]

		return newFreq



class VegenereSecret(object):
	def __init__(self,diff,key):
		self.freqDiff = diff
		self.key = key

	def print(self):
		print(self.freqDiff,self.key)


class SortedQueue(object):
	def __init__(self, maxsize):
		self.maxSize = maxsize
		self.curSize = 0
		self.container=[]

	def remove(self,index):
		assert index >=0 and index< self.curSize,"invlaid index Error!"
		temp = self.container[:index]
		if index<maxsize-1:
			temp += self.container[index+1:]
		self.container=temp
		self.curSize-=1

	def getVal(self,index):
		assert index >=0 and index< self.curSize,"invlaid index Error!"
		return self.container[index].key

	def print(self):
		print("\n............")
		for i in range(self.curSize):
			ele = self.container[i]
			ele.print()
		print("............\n")

	def insertPreferSmaller(self,ele):
		assert type(ele) is VegenereSecret,"inserted element must be VegenereSecret type"
		if self.curSize < self.maxSize:
			isInserted = False
			for i in range(self.curSize):
				curEle = self.container[i]
				if ele.freqDiff <= curEle.freqDiff:
					temp = self.container[:i]
					temp.append(ele)
					temp += self.container[i:]
					self.container = temp
					self.curSize+=1
					isInserted=True
					break
			if not isInserted:
				self.container.append(ele)
				self.curSize+=1
		else:
			for i in range(self.curSize):
				curEle = self.container[i]
				if ele.freqDiff <= curEle.freqDiff:
					temp = self.container[:i]
					temp.append(ele)
					temp += self.container[i:self.maxSize-1]
					self.container = temp
					break

	def insertPreferGreater(self,ele):
		assert type(ele) is VegenereSecret,"inserted element must be VegenereSecret type"
		if self.curSize < self.maxSize:
			isInserted = False
			for i in range(self.curSize):
				curEle = self.container[i]
				if ele.freqDiff > curEle.freqDiff:
					temp = self.container[:i]
					temp.append(ele)
					temp += self.container[i:]
					self.container = temp
					self.curSize+=1
					isInserted=True
					break
			if not isInserted:
				self.container.append(ele)
				self.curSize+=1
		else:
			for i in range(self.curSize):
				curEle = self.container[i]
				if ele.freqDiff > curEle.freqDiff:
					temp = self.container[:i]
					temp.append(ele)
					temp += self.container[i:self.maxSize-1]
					self.container = temp
					break




