'''

This code uses a wrapper function which calls in FFT & IFFT func implemented in C and helps in running in python.


Resourses : 
Warning : Make sure that .so file and .py have different titles during importing !!

https://stackoverflow.com/questions/65356321/creating-a-python-module-using-ctypes
https://medium.com/spikelab/calling-c-functions-from-python-104e609f2804
'''


from ctypes import CDLL, c_double
import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes


_fftlib = ctypes.CDLL('./fftlib_wrapper.so')


def find_FFT(z):
	global _fftlib
	n = len(z)

	_fftlib.FFT.argtypes = ( ndpointer(dtype=np.complex128, ndim=1, flags='C',shape=(n,)), 
			 ctypes.c_int)

	_fftlib.FFT.restype = ndpointer(dtype=np.complex128, ndim=1, flags='C',shape=(n,))

	Z = _fftlib.FFT(z,n)
	return Z


def find_IFFT(z):
	global _fftlib
	n = len(z)

	_fftlib.IFFT.argtypes = ( ndpointer(dtype=np.complex128, ndim=1, flags='C',shape=(n,)), 
			 ctypes.c_int)

	_fftlib.IFFT.restype = ndpointer(dtype=np.complex128, ndim=1, flags='C',shape=(n,))

	Z = _fftlib.IFFT(z,n)
	return Z

	

'''
#An example..  Uncomment to run

if __name__ == "__main__":
	z = np.array([1,2,3,4,2,1,0,0],dtype =np.complex128 )
	Z = find_FFT(z)
	print("FFT of z :\n")
	print(Z)
	z_cap = find_IFFT(Z)
	print("IFFT of Z\n")
	print(z_cap)
'''
