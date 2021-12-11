import numpy as np
import matplotlib.pyplot as plt
import cmath

'''

Section 3.1.2
Generates plots for differnet lowpass chebychev filters for order N = 4

Range of eps is derived from para.py
|H(omega)|^2 = 1/ (1+ (eps* C_n(omega_l/Omega_lp)^2 ))
'''

if __name__ == "__main__":
	N = 4
	eps  = np.arange(0.35, 0.61, 0.05)
	omega = np.linspace(0,2,201)
	H = np.zeros((eps.size,omega.size))

	for i in range(len(eps)):
		for j in range(len(omega)) : 
			H[i][j] =  np.real(1/np.sqrt(1 + eps[i]**2*np.cosh(N*cmath.acosh(omega[j]))**2))
		plt.plot(omega,H[i,:])
		
	plt.grid()

	plt.legend(["$\epsilon$ = 0.35", "$\epsilon$ = 0.40","$\epsilon$ = 0.45","$\epsilon$ = 0.50","$\epsilon$ = 0.55","$\epsilon$ = 0.60"], loc ="upper right")
	plt.xlabel("$\Omega$")
	plt.ylabel("$|H_{a,LP}(j\Omega)|$")
	plt.title("Lowpass Chebyshev filter plots of order N = 4 \nfor different $\epsilon$ values ")
	#plt.show()
	plt.savefig('figs/parameter_plots.eps')
	
