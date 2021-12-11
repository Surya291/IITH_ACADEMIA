'''
Section 3.1.3 
finds the low pas chebychev filter by obtaining beta , r1, r2 returns gain(G)
range of eps and N are found in para.py
'''

def lp_stable_cheb(eps,N):
	import numpy as np 
	beta = (( np.sqrt(1+eps**2) +1) /eps) **(1/N)
	r1 = (beta**2-1)/(2*beta)
	r2 = (beta**2+1)/(2*beta)
	
	### Computing the polynom in denom of H
	u = 1
	for n in range( int(N/2)):
		phi = np.pi/2 + (2*n+1)*np.pi/(2*N)
		### Coeffs
		v = [1,(-2*r1)*np.cos(phi),(r1**2)*((np.cos(phi))**2) + (r2**2)*((np.sin(phi))**2)] 
		p = np.convolve(v,u)
		u = p
	
	### Computing gain 
	G = abs(np.polyval(p,1j))/np.sqrt(1+eps**2)
	return p,G


	
if __name__ == "__main__":
	import numpy as np
	print(lp_stable_cheb(0.4, N=4))
		
	
	
	
