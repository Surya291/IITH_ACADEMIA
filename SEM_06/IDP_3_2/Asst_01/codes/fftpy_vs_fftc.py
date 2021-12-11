'''

This code demonstrates the run-time analysis for the recursive FFT algorithm implemented in python(alone) vs 
the same algorithm implemented in C and run in python through wrapper functions.

Result  : We can observe that the C implementation is faster although its the same algorithm.

'''

import time
import numpy as np
import matplotlib.pyplot as plt
import fftlib

def FFT_recur(x):
    N = x.shape[0] 
    X = np.zeros(x.shape,dtype = 'complex_')

    if N==1:
        return x
    
    else:
        X_e = FFT_recur(x[0::2])
        X_o = FFT_recur(x[1::2])
        
        W = np.array([np.exp(-1j*2*np.pi*k/N) for k in range(int(N/2))])
        
        X = np.concatenate([X_e + W*X_o,X_e - W*X_o])  ### Exploiting symmetry : e^(j*2pi*k/N) = -1* e^(j*2pi*(k+N/2)/N)
        
    return X

#### Run time comparisions :
R = 9

t_DFT = np.zeros(R)
t_FFT = np.zeros(R)
t_FFT_C = np.zeros(R)

for r in range(2,R+2):
    N = 2**r
    x = np.random.randint(1,10,N)

    t1 = time.time()
    X_fft = FFT_recur(x)
    t2 = time.time()
    X_fft_c = fftlib.find_FFT(x.view(np.complex128))  ### inpit should be a complex no.
    t3 = time.time()

    t_FFT[r-2] = t2 - t1
    t_FFT_C[r-2] = t3 - t2
    
    
    
R_vec = np.arange(2,R+2)
plt.xlabel('\u03B3')
plt.ylabel('Run time in secs')
plt.title('Run time comparisions for FFT algo \n  implemented in C & Py  wrt \u03B3 \nwhere N = 2^\u03B3')

plt.plot(R_vec,t_FFT,label = 'FFT_py')
plt.plot(R_vec,t_FFT_C,label = 'FFT_C')
plt.grid()
plt.legend()  
plt.savefig('../figs/fftpy_vs_fftc.eps')  


