import numpy as np
import math

def entropy(d):
	ent =0
	for x in d:
		if x==0: temp =0
		else:temp  = -1*x*math.log2(x)
		ent +=temp
	return ent

file  = open("file1.txt", "r")
data = file.read()
l = len(data)
d= [0]*256
count =0
for i in range(l):

	alpha = ord(data[i])
	if alpha<256:
		d[alpha] +=1
		count+=1

print([x/l for x in d])
print(entropy(d))
print(count)
