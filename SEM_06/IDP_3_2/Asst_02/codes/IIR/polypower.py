
'''
Helper func used in bilin.py
'''
import numpy as np
def polypower(v,N):
	y = np.array([1])
	if (N > 0):
		for i in range(N):
			y = np.convolve(y,v)
	return y

