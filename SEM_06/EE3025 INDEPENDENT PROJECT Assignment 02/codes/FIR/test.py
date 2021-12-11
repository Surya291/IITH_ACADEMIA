import numpy as np
import matplotlib.pyplot as plt

'''
This program returns the filter coeff for a bandpass filter designed using a kaiser window(Low pass) later
converted to a bandpass .

All the notations follow the design specifications , mentioned in write-up
'''


pi = np.pi

## Filter no 
L = 114

### Sampling freq
Fs = 48

### const
const = 2*pi/Fs;

### delta : tolerance
delta = 0.15

### finding filter passband freqs
F_p1 = 3 + 0.6*(L-107)
F_p2 = 3 + 0.6*(L-109)

delF = 0.3

#### findign filter's stop band freq
F_s1 = F_p1 + delF
F_s2 = F_p2 - delF

### Normalised freq
omega_p1 = const*F_p1
omega_p2 = const*F_p2


omega_c = (omega_p1+omega_p2)/2
omega_l = (omega_p1-omega_p2)/2
omega_s1 = const*F_s1
omega_s2 = const*F_s2
delomega = 2*pi*delF/Fs

A = -20*np.log10(delta)

N = 100

n = np.arange(-N,N)
hlp = np.sin(n*omega_l)/(n*pi)

hlp[N] = omega_l/pi

G = 1/np.sum(hlp)

### Low pass 
hlp = G*hlp

###  band pass equivalent
hbp = 2*hlp*np.cos(n*omega_c)

omega = np.linspace(-pi/2,pi/2,200)

### finding the band pass freq response
Hbp = np.polyval(hbp,np.exp(-1j*omega))
Hlp = np.polyval(hlp,np.exp(-1j*omega))


### Plotting low pass equivalent
plt.figure(1)
plt.grid()
plt.plot(omega/pi,np.abs(Hlp))
plt.xlabel('$\omega/\pi$')
plt.ylabel('$|H_{lp}(\omega)|$')
plt.title("Magnitude response of FIR lowpass (equivalent) filter")
plt.savefig('figs/FIR_lowpass.eps')

### Plotting band pass equivaling
plt.figure(2)
plt.grid()
plt.plot(omega/pi,np.abs(Hbp))
plt.xlabel('$\omega/\pi$')
plt.ylabel('$|H_{bp}(\omega)|$')
plt.title("Magnitude response of FIR Bandpass filter")
plt.savefig('figs/FIR_bandpass.eps')


### Saving coeff..
fir_coeff = hbp
np.savetxt("fir_coeff.dat", fir_coeff)
