def shiftText(inp,shift):
    data = []
    for i in inp:   #iterate over the text not some list
        if i.strip() and i in alpha: # if the char is not a space ""  
            data.append(alpha[(alpha.index(i) + shift) % 26])    
        else:
            data.append(i)
    output = ''.join(data)
    return output

def crackCaesarCipher(cipher):
	for i in range(26):
		print(shiftText(cipher,i))

crackCaesarCipher("QEB NRFZH YOLTK CLU GRJMP LSBO QEB IXWV ALD")