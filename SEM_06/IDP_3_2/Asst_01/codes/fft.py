########################################
####  This code implements a recursive N-point FFT ;  N = 2^k ==> k is an integer  with 'real' time domain 
#### X = FFT(x)   ===>>>  x = scaling_factor* FFT(conj(X))
####   By Koidala Surya Prakash -- ee18btech11026@iith.ac.in
########################################

import numpy as np
import matplotlib.pyplot as plt
#If using termux
import subprocess
import shlex
#end if


N = 8   ### Should be pow of 2

pad = 2  ### no. of padding depending on input 
n = np.arange(N-pad)
fn=(-1/2)**n
hn1=np.pad(fn, (0,pad), 'constant', constant_values=(0))
hn2=np.pad(fn, (pad,0), 'constant', constant_values=(0))
h = hn1+hn2

xtemp=np.array([1.0,2.0,3.0,4.0,2.0,1.0])
x=np.pad(xtemp, (0,pad), 'constant', constant_values=(0))

def FFT_recur(x):
    N = x.shape[0] 
    
    if N ==2:  ## Base case..
        return np.array([[1,1],[1,-1]])@x  ### A 2 point dft
    
    else:
        X_e = FFT_recur(x[0::2])
        X_o = FFT_recur(x[1::2])
        
        W = np.array([np.exp(-1j*2*np.pi*k/N) for k in range(int(N/2))])
        
        X = np.concatenate([X_e + W*X_o,X_e - W*X_o])  ### Exploiting symmetry : e^(j*2pi*k/N) = -1* e^(j*2pi*(k+N/2)/N)
        
    return X

def IFFT_recur(X):
    N= X.shape[0]
    x = (1/N)*FFT_recur(np.conj(X)) ### Exploting the fact that x is Real : x = FFT(conjugate(X))
    return np.real(x)
    
print('x = ',np.round(x,3))
print('h = ',np.round(h,3))



X = FFT_recur(x)
H = FFT_recur(h)
Y = X*H
y = IFFT_recur(Y)

print('X[k] = ',np.round(X,3))
print('H[k] = ',np.round(H,3))
print('y = ',y)
#plots
plt.stem(range(0,N),y,use_line_collection = True)
plt.title('Filter Output using 8 point FFT')
plt.xlabel('$n$')
plt.ylabel('$y(n)$')
plt.grid()# minor
plt.savefig('../figs/fft.eps')
#
#If using termux
#plt.savefig('../figs/yndft.pdf')
#subprocess.run(shlex.split("termux-open ../figs/yndft.pdf"))
#else
#plt.show()


