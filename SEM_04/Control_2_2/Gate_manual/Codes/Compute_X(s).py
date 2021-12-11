'''
Code for finding X(s) from a given state space model equation

By Koidala Surya Prakash
Dated Apr 16, 2020
Released Under GNU GPL

'''
import sympy as sp
import numpy as np

s = sp.Symbol('s')

def compute_X(A,B,x_0,U_s):
    k = len(A)
    I = sp.eye(k)
    X = ((((s*I - A)**-1) * B * U_s) + ((s*I - A)**-1)*x_0)
    return X
A = np.array([[0,0],
             [0,-9]]) # Input A matrix
B = np.array([[0],
              [45]]) # Input B matrix
x_0 = np.array([[0],
                [0]])# Input initial comditions
U_s = 1/s            # Input U(s)
X = compute_X(A,B,x_0,U_s)
X = np.array(X)      # It is the required X(s) matrix
print('X(s) = ')
print(X)
