'''
A helper func generating the coeff of a chebychev poly with an order N
'''
import numpy as np
def cheb(N):
	v = np.array([1,0])
	u = np.array([1])
	
	if N == 0:
		w = u
	elif N==1:
		w = v
	else:
		for i in range(N-1):
			p = np.convolve(np.array([2,0]),v)
			m,n = len(p), len(u)
			w = p + np.append(np.zeros(m-n),u)
			u = v
			v = w
	return w
			

if __name__ == "__main__":
	import numpy as np
	
	print(cheb(4))
