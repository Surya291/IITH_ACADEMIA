###################################################################

# This a python code for verification of the final value theorem 
# By Koidala Surya Prakash
# April 16 , 2020 
# Released under GNU GPL

###################################################################

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,2,1000)
x1 = 0*t                ## We evaluated : x1(t) = 0
x2 = 5*(1-np.exp(-9*t)) ## Finding the time domain signal of X(s) using inverse laplace transform.

y = np.sqrt((x1)**2+(x2)**2)## ploting the required function.

plt.plot(t,y)
plt.xlabel('t')
plt.ylabel('y = ((x1(t))^2  +(x2(t))^2)^0.5')
plt.show()

#####################################################################

## Result to be observed :
# We find that y(t) reaches 5 as t--> infinity
# Hence our theoritical result matches the plot.
