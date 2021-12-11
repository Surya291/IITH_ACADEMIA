/*
####  This code implements a recursive N-point FFT ;  N = 2^k ==> k is an integer  with 'real' time domain 
#### X = FFT(x)   ===>>>  x = scaling_factor* FFT(conj(X))
####   By Koidala Surya Prakash -- ee18btech11026@iith.ac.in



Note : 

 To run : 
>> gcc my_fft.c -lm -o a.out
>> ./a.out
*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <complex.h>


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

	return x;
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

int main()
{

	//int n = 2;
	int n = 8;
	cp x[] = {1,2,3,4,2,1,0,0};
	
	printf("\nFFT is \n");

	cp *X_FFT = FFT(x,n);


	for (int j=0;j<n;j++)
	{

        	printf("[%.4lf, %.4lf]\n", creal(X_FFT[j]), cimag(X_FFT[j]));
	}

	cp *x_cap = IFFT(X_FFT,n);

	printf("\n IFFT is \n");

	for (int j=0;j<n;j++)
	{

        	printf("[%.4lf, %.4lf]\n", creal(x_cap[j]), cimag(x_cap[j]));
	}


		
	return 0;

	
	

}
