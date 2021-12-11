import numpy as np
import cmath

'''
Computes the range of eps to deisign a lowpass chebychev for given design parameters..
Corresponds to Sec 3.1.1 & 3.1.2
'''


pi = np.pi
# Filter no.
L = 114

## Sampling freq
Fs = 48

## Scaling constant for notmalising
const = 2*pi/Fs

### delta : tolerance
delta = 0.15

### finding filter passband freqs
F_p1 = 3 + 0.6*(L-107)
F_p2 = 3 + 0.6*(L-109)

delF = 0.3

#### findign filter's stop band freq
F_s1 = F_p1 + delF
F_s2 = F_p2 - delF

### Normalised freq (both pass and stop band)
omega_p1 = const*F_p1
omega_p2 = const*F_p2

omega_s1 = const*F_s1
omega_s2 = const*F_s2

### finding analog filter freq from normalised freq :: OMEGA = tan(omega/2)
OMEGA_p1 = np.tan(omega_p1/2)
OMEGA_p2 = np.tan(omega_p2/2)

OMEGA_s1 = np.tan(omega_s1/2)
OMEGA_s2 = np.tan(omega_s2/2)


### computing center freq and bandwidth
OMEGA_0 = np.sqrt(OMEGA_p1*OMEGA_p2)


print("OMEGA_0", OMEGA_0)
print("OMEGA_p2", OMEGA_p2)
B = OMEGA_p1 - OMEGA_p2
print("B = ",B)
## lowpass stopband freq
OMEGA_L = min(abs( (OMEGA_s1**2 - OMEGA_0**2)/(B*OMEGA_s1) ), abs( (OMEGA_s2**2 - OMEGA_0**2)/(B*OMEGA_s2) ) )
print("Omega_l = ",OMEGA_L)

D1 = 1/((1-delta)**2) - 1
D2 = 1/(delta**2) -1


## Finding lower bound of order of chebychev filter
N = np.ceil(np.real(cmath.acosh(np.sqrt(D2/D1))/cmath.acosh(OMEGA_L)))
print("Min order of the chebychev filter is : ", N)

### Finding range of eps
eps1 = np.real(np.sqrt(D2)/np.cosh(N*cmath.acosh(OMEGA_L)))
eps2 = np.real(np.sqrt(D1))

print("Range of eps : [%.3f,%.3f]"%(eps1,eps2) )




