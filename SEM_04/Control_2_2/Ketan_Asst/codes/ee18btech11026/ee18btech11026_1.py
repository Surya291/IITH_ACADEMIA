import numpy as np
OS = 0.55
zeta = -np.log(OS)/(np.sqrt((np.pi)**2 + (np.log(OS))**2))
phi_m = np.arctan(2*zeta/(np.sqrt(-2*(zeta**2)+np.sqrt(4*(zeta**4)+ 1))))*(180/np.pi);

print("Damping ratio = ",zeta)
print("Phase margin(in degrees) = ",phi_m)
