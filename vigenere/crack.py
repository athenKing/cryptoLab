# import functions
from definitions import Frequency,VegenereSecret,SortedQueue
from vigenere import VigenereAlgorithm

odd = "DWFOSZPFWGVVMVOBXTBMGIILECURUWKGZGNMUHUHMKDTNUWDRMGHPTQABVVKOTVOAMKHCGJWGUGMEWQGIOAGSCLVSLGIQKFDIEUQXUHWCSWVGGARMMVVFWAJKICMUROBLYVQYFBAGGGFUMFYCZXTEXNZMAPCZJTWENWLVHZNOATEHQBOABVGBVMTLWTNRSAYTCUGIMBPVMEFVMYSIXOMLUSABGBAGHZHTBUCGMQNWWGZKBNXEGHMYZVHPFMIFZLKPTRUZTPGIPUQHPGIEFVHVFMNMTRRCAFJJEGGQADMYKBIADQTNWVFUQMWHQBOAVCBVBUIOQWLZFLBCHQAHLBUDCGFAMJSKBTBHHAMQJIMKCVVOKKGOARTBKCBANDBBQBKBTBLNWUVUQGIHPRNQGKACZQZTEHQPBTMTOVFBKMKCVFJHXCBLPVBMKBOBGNMJSXBTABDWTVUGYQFAZBTEEOAHBTMTOVFBKMKCVFBVWVVMEFQLCPZBBLXTQWFUQGVVMYPALQTIOJTBVMBBNIDGBWASMOGFAVCTXROGZFVMUTWEOWGTSDRSABDZMFFZOKQMFXQMJHPRQWLUWJVMQMACNEFDXTGIYUPXPSMQGWKVFCFUAITSIQTUXTQPNOBLOIAGCMPCFGBGBAGWZPVAMQAMETPTUGTVOOMJSUSPZFQFMVONHTAIGJWGVVIAUPXAKWHMLHVVMEXQLGBMREIVGFBNJVIGFKROBTISWSGZTWRQFBKVGDBREILWBIIPQWCPTRUPXUSKBTBLCBLCBGFGBBHOKXTHIVOBBGGKNOJXCJWVEMWKBXRSAHPPGHTQGIDPLTQVCZKHSZXPQGOVBGQAMPIIGKGURYQLVGBBNIDGDILNMGVGWIFZTECUZVVBEOBVPVLEVIAOMEYWBUPCMCHZHTBXFDIEUG"

even = "ZMJXCGLHBGIPSPMPSOUQEOQYIFRYWCYVBWBVQKICRMWUEDXYCVAMRRYMCSRFMBGRNTLGTXRVJQKENAIFQZIIIJTATEHMUMVYZCZWPVHGLQUAOQDMVTBWBQAFJOXKVNQQTENVWACXBZRITVROUWLKJMBVRFWJXQYPWTKOIEFXKFLSBFKTTXVVFLVZKVMGQREEXQPPSEHBYIAVIBOHCJIFBVGHFPTSOFMFPLICERITWPDBZSPLIGEHUFXGVIGUGQJTGGASEVIEHEHUDHWMIXGKUWADTJMPMCFAVCTLCIXZVFIKMQGAQEHIKICGMSQIWIRGPBMCHAFJEKGDGROIERAQQFBAKIOLEVVFPDMPBUWMHBYIPXKSFVQKCQYASPXZVOGRLWFWZZFWMQCAFPRRPXTGNQLJYRITMGKMVUWBDOYHVKSHTEFVWBVRUBOBNWCIICMBVRVIDIVBUSGKMFVGMQQNOLVZGEWDZHVKWKGQBSRZDEVBWBGKMFVATVRPRUGYVXZGPLMEGGLPCJSZFQKLMCSSZFZKWQBTSZFZCUTMFHKLVGVZMCWWJCUMMAFFPRRIBVUGKQJEPVQSAWIIXKGBCNVKZIPVMHUHLVZGEWDZHVKSHVWACXBVVEHVHERTCIFVWAZXVZGCMQCAQMKAQKSGCUWEWGLMTSRZKPGLAOAGQEIZIMBFLDVGQGBOPWJVXYXMBCHWGPGHZQBPXLXGKACARXGSUBBSFLLVWQYBVRZWIPFKMDYDKZRIFWGGPIZPCGLANQGVBENZGVRVJAKMPHROMTSOFCBVFIKMQGATBUURRATXDYLKRXKHVGGKMJIEHVHNFBJQWLBPRPIUIUXKIEHIXEKGAHORBYICOMGQUWGTKGOOAGBYIKGRSPWQFRQYQZYHOZXKFIHRPMJWCZMGNWXIIUXVHU"

class CrackVigenere(object):
	def __init__(self):
		self.alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		self.eng_freq = [.0817, .0149, .0278, .0425, .1270, .0223, .0202, .0609, .0697, .0015, .0077, .0403, .0241, .0675, .0751,
            .0193, .0010, .0599, .0633, .0906, .0276, .0098, .0236, .0015, .0197, .0007]
		self.vigenere = VigenereAlgorithm()

	def friedmanTest(self,cipher):
		assert len(cipher) >2, "cipher length must be greater than 2"
		N = len(cipher)
		# print("cipher length is: ",len(cipher))
		cipherDict={}
		for v in self.alpha:
			cipherDict[v]=0
		for i in range(N):
			cipherDict[cipher[i]]+=1
			
		# print(cipherDict)

		k_0 = 0
		for k,v in cipherDict.items():
			k_0+=v*(v-1)
		k_0 /= (N*(N-1))

		# print("k_0 is: ",k_0)
		k_p = .067
		k_r = .0385
		L = (k_p - k_r)/(k_0-k_r)
		print("Approximate key length is: ",L,"\n")

	#returns the possible key length
	def KasiskiTest(self,cipher):
		assert len(cipher) >2, "cipher length must be greater than 2"

		print("cipher length is: ",len(cipher),"\n")

		cipherDict={}
		cipherLen = len(cipher)-3
		for i in range(cipherLen):
			curTrigraph = cipher[i:i+3]
			if  curTrigraph in cipherDict:
				cipherDict[curTrigraph].append(i)
			else:
				cipherDict[curTrigraph]=[i]

		deltes = []
		remains = []
		for k,v in cipherDict.items():
			if len(v) == 1:
				deltes.append(k)
			else:
				remains.append(k)
		for d in deltes:
			del cipherDict[d]

		##Calculate the distance of trigraph strings
		for k in remains:
			length = len(cipherDict[k])
			for i in range(length):
				mirror_i = length-i-1
				if mirror_i==0:
					cipherDict[k].pop(0)
					break
				else:
					cipherDict[k][mirror_i]=cipherDict[k][mirror_i]-cipherDict[k][mirror_i-1]

		# print(cipherDict)

		filterList = SortedQueue(maxsize=10)
		keyLenOptions=[]
		for v in range(3,100):
			keyLenOptions.append(v)

		for keyLen in keyLenOptions:
			count=0
			for _,listVal in cipherDict.items():
				for v in listVal:
					if v%keyLen == 0:
						count+=1
			filterList.insertPreferGreater(VegenereSecret(count,keyLen))

		filterList.print()

	def calcSingleNearestFreq(self,listVal):
		calc={}
		P=[]
		N = len(listVal)
		for v in self.alpha:
			calc[v]=0
		for i in range(N):
			calc[listVal[i]]+=1

		for v in self.alpha:
			# calc[v]/=N
			P.append(calc[v])

		offset = 0
		sumVal = 0

		optionKeys = SortedQueue(maxsize=3)

		offsetCurP=[]
		for i in range(26):
			curP = P[i:]+P[:i]
			curSum=0
			for j in range(26):
				curSum += self.eng_freq[j]*curP[j]
			optionKeys.insertPreferGreater(VegenereSecret(curSum,(26-i)%26))

		return optionKeys

	# def calcTotalNearestFreq(self,matrix,ifKeyLen):
	# 	for i in range(26):
	# 		eng_freq[i] *= cipherLen

	# 	optionKeys = SortedQueue(maxsize=10)
	# 	frequences=[]

	# 	for row in range(ifKeyLen):
	# 		init = {}
	# 		for letter in alpha:
	# 			init[letter]=0
	# 		cur = matrix[row]
	# 		for c in cur:
	# 			init[c] += 1
	# 		frequency = Frequency()
	# 		for letter in alpha:
	# 			frequency.insertPreferSmaller(init[letter])
	# 		frequences.append(frequency)

	# 	ups=[]
	# 	lows=[]
	# 	for j in range(ifKeyLen):
	# 		ups.append(26**(j+1))
	# 		lows.append(26**j)

	# 	for i in range(26**ifKeyLen):
	# 		#Below is the index of the current round offset
	# 		if i%10000==0:
	# 			print(i)
	# 		indexes = []
			
	# 		totalFrequency=Frequency()
	# 		for j in range(ifKeyLen):
	# 			index = (i%ups[j])//lows[j]
	# 			# print(index)
	# 			indexes.append(index)
	# 			totalFrequency +=  frequences[j].shift(index)

	# 		#This approximity meansurement maybe too coarse
	# 		diff = totalFrequency.countDiff(Frequency(eng_freq))
	# 		option = VegenereSecret(diff,indexes)
	# 		optionKeys.insert(option)

	# 	return optionKeys

	def filterAgain(self,matrix,options,ifKeyLen,base,limit):
		result = SortedQueue(maxsize=limit)
		frequences=[]
		for row in range(ifKeyLen):
			init = {}
			for letter in alpha:
				init[letter]=0
			cur = matrix[row]
			for c in cur:
				init[c] += 1

			frequency = Frequency()
			for i,letter in enumerate(alpha):
				frequency.put(i,init[letter])
			frequences.append(frequency)

		ups=[]
		lows=[]
		for j in range(ifKeyLen):
			ups.append(base**(j+1))
			lows.append(base**j)

		for i in range(base**ifKeyLen):
			#Below is the index of the current round offset
			totalFrequency=Frequency()
			indexes =[]
			for j in range(ifKeyLen):
				baseIndex = (i%ups[j])//lows[j]
				index = options[j].getVal(baseIndex)
				totalFrequency +=  frequences[j].shift(index)
				indexes.append(index)

			#This approximity meansurement maybe too coarse
			diff = totalFrequency.countDiff1(Frequency(eng_freq))
			option = VegenereSecret(diff,indexes)
			result.insertPreferGreater(option)

		return result

	def crack(self,cipher,ifKeyLen,singleRoom,totalRoom):
		matrix=self.vigenere.getMatrix(cipher,ifKeyLen)

		#find hightest coefficients seperately
		options=[]
		for row in range(ifKeyLen):
			option = self.calcSingleNearestFreq(matrix[row])
			options.append(option)

		offsets=[]
		for option in options:
			# option.print()
			offsets.append(option.getVal(0))

		keyString=''
		for a in offsets:
			keyString+=self.alpha[a]
		
		result = self.vigenere.encrypt(cipher,keyString)

		print(result)



cur = odd
cur = even

crack = CrackVigenere()
crack.friedmanTest(cur)
crack.KasiskiTest(cur)
crack.crack(cur,9,3,20)