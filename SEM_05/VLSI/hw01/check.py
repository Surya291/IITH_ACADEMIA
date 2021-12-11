import numpy as np
f1 = 'vout.dat'

vin_dat = np.loadtxt(f1,usecols = (1))
vout_dat = np.loadtxt(f1,usecols = (3))

t_find = np.loadtxt(f1,usecols = (0))

t_in = np.amin(np.where( abs(vin_dat-0.5) < 0.001))
t_out = np.amin(np.where( abs(vout_dat-0.5) < 0.001))

print(t_find[t_in])


