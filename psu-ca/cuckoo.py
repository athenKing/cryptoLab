def hash1(x):
	return (x-1) % 6

def hash2(x):
	return (x*2) % 6



val = [3, 7, 14]


filter = [0,0,0,0,0,0]

while len(val) >0:
	v = val.pop(0)

	v1 = hash1(v)
	v2 = hash2(v)

	if filter[v1] == 0:
		filter[v1] = v
	elif filter[v2] == 0:
		filter[v2] = v
	else:
		y = filter[v2]
		val.insert(0,y)
		filter[v2] = v


print(filter)


