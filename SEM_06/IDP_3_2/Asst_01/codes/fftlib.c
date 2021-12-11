/*
####  This code implements a recursive N-point FFT ;  N = 2^k ==> k is an integer  with 'real' time domain 
#### X = FFT(x)   ===>>>  x = scaling_factor* FFT(conj(X))
####   By Koidala Surya Prakash -- ee18btech11026@iith.ac.in
*/

#include <stdio.h>
#include <complex.h>
#include <stdlib.h>
#include <math.h>

typedef double complex cp;
# define pi 3.141592653589793238



cp *FFT(cp *x, int n)
{
	if (n<=1)
		return x;

	cp *X_even = malloc( (n/2) * sizeof(cp));
	cp *X_odd = malloc( (n/2) * sizeof(cp));

	for (int i =0;  i < n/2;i++)
	{
		X_even[i] = x[2*i];
		X_odd[i] = x[2*i + 1];
	}

	X_even = FFT(X_even, n/2);

	X_odd = FFT(X_odd , n/2);

	for (int i=0; i<n/2 ;i++)
	{
		cp w = CMPLX( cos(2*pi*i/n), -1*sin(2*pi*i/n) );
		x[i] = X_even[i] + w*X_odd[i] ;
		x[i+ (n/2)] = X_even[i] - w*X_odd[i];
	}
	
	free(X_even);
	free(X_odd);

	return x ;
}



cp* IFFT (cp *X, int n) // This func uses FFT function itself by exploiting the signal being real.
{
	cp c = n;       // Helps in less code in a hardware setup

	for (int i = 0; i< n ; i++)
	{
		X[i] = (1/c)*conj(X[i]);
	}

	X = FFT(X,n);

	return X;
	

}

