'''
Helper func used in bilin.py
'''

import numpy as np
def add(x,y):
    m,n = len(x),len(y)
    
    if m==n:
        z = np.array(x)+np.array(y)
    elif m>n : 
        z = np.array(x) +  np.array([0]*(m-n) + y)
    else: 
        z =   np.array([0]*(n-m) + x) + np.array(y)
        
    return z


if __name__ == "__main__":
	import numpy as np 
	a = [1,2,3]
	b = [1,2]

	print((add(a,b)))
