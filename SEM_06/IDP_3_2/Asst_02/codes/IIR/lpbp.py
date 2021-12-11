'''
Converts low pass to bandpass  equivalent : Section 3.1.4
The analog bandpass is obtained from its lowpass equivalent .. whose TF is computed in para.py
This is converted by substituting s = (s^2 + OMEGA_0^2 / Bs)

For Notations please refer to the writeup

p -- >denomination polynomial coeff
B = Band width of the lp filter computed in para.py
OMEGA_0  & OMEGA_P2  computed in para.py 

returns G_bp, num, dem of bandpass filter TF
'''
import numpy as np



def lpbp(p,OMEGA_0,B,OMEGA_p2):

	N = len(p)
	const = np.array([1,0,OMEGA_0**2])
	v = np.array([1,0,OMEGA_0**2])

	
	if N > 2:
		for i in range(N-1):
			M = len(v)
			v[M-i-2] = v[M-i-2] + p[i+1]*(B**(i+1))
			if i < N-2:
				v = np.convolve(const,v)
		den = v
		
	elif N == 2:
		M = len(v)
		v[M-2] = v[M-2] + p[N-1]*B
		den = v
	else :
		den = p
	
	num = np.concatenate((np.array([1]),np.zeros(N-1)))
	G_bp = abs(np.polyval(den,1j*OMEGA_p2)/(np.polyval(num,1j*OMEGA_p2)))
	return num,den,G_bp
	
if __name__ == "__main__":
	import numpy as np

	#Param obtained through runing earlier codes 

	p = np.array([1.        , 1.10677989, 1.61248087, 0.91402101, 0.3365728 ])
	OMEGA_0 = 0.4594043442925196
	OMEGA_p2 = 0.41421356237309503
	B =  0.09531188712133376
	print(lpbp(p,B,OMEGA_0,OMEGA_p2))


 
		
		
			
	
