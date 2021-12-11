'''
Uses all the functions and 
'''

import numpy as np
import matplotlib.pyplot as plt
from para import *
from lp_stable_cheb import lp_stable_cheb
from lpbp import lpbp
from bilin import bilin

print(OMEGA_0)
eps = 0.4
### plotting low pass filter mag plot
[p,G_lp] = lp_stable_cheb(eps,N)
OMEGA_L = np.linspace(-2,2,401)
H_analog_lp = G_lp*abs(1/np.polyval(p,1j*OMEGA_L))

plt.figure(1)
plt.grid()
plt.plot(OMEGA_L,H_analog_lp)
plt.xlabel('$\Omega$')
plt.ylabel('$|H_{a,LP}(j\Omega)|$')
plt.title('Analog Lowpass Chebyshev filter ')
plt.savefig('figs/Analog_IIR_lowpass.eps')


#plotting analog bandpass filter mag plot

[num,den, G_bp] = lpbp(p,OMEGA_0,B,OMEGA_p1)
OMEGA = np.arange(-0.65,0.65,0.01)
H_analog_bp = G_bp*abs(np.polyval(num,1j*OMEGA)/np.polyval(den,1j*OMEGA))

plt.figure(2)
plt.grid()
plt.plot(OMEGA,H_analog_bp);
plt.xlabel('$\Omega$')
plt.ylabel('$|H_{a,BP}(j\Omega)|$')
plt.title('Analog bandpass Chebyshev filter ')
plt.savefig('figs/Analog_IIR_Bandpass.eps')


#plotting digital bandpass filter mag plot


[dignum,digden,G] = bilin(den,OMEGA_p1)
OMEGA = np.arange(-2*np.pi/5,2*np.pi/5, pi/1000)
H_dig_bp = G*abs(np.polyval(dignum,np.exp(-1j*OMEGA))/np.polyval(digden,np.exp(-1j*OMEGA)))
iir_num = G*dignum
iir_den = digden

plt.figure(3)
plt.grid()
plt.plot(OMEGA/pi,H_dig_bp)
plt.xlabel('$\omega/\pi$')
plt.ylabel('$|H_{d,BP}(\omega)|$')
plt.title('Digital bandpass Chebyshev filter')
plt.savefig('figs/Digital_IIR_Bandpass.eps')

np.savetxt("dat_files/iir_num.dat",iir_num)
np.savetxt("dat_files/iir_den.dat",iir_den)
np.savetxt("dat_files/dignum.dat",dignum)
np.savetxt("dat_files/digden.dat",digden)
np.savetxt("dat_files/G.dat",np.array([G]))

