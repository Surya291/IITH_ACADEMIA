

'''
Converts the obtained analog bandpass filter into a digial pandpass filter
returns num, denom , G for the digital version 

H(z) = G* dignum(z)/ digden(z)
'''
from add import add
from polypower import polypower
import numpy as np

def bilin(p,om):
	import numpy as np
	N = len(p)
	const = np.array([-1,1])
	v = 1
	if (N>2):
		for i in range(1,N):
			v = np.convolve(const,v)
			v = add(v, p[i]*polypower([1,1], i))
		digden = v
	elif N==2 :
		M = len(v)
		v[M-2] = v[M-2] + p[N-1]
		v[M-1] = v[M-1] + p[N-1]
		digden = v
	else:
		digden = p
	dignum = polypower([-1,0,1],int((N-1)/2))
	G = abs(np.polyval(digden,np.exp(-1j*om))/np.polyval(dignum,np.exp(-1j*om)))
	return dignum,digden,G
	
	
	
	
	
