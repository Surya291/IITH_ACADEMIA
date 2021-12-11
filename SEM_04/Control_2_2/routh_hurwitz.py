import numpy as np
import tensorflow as tf


#c = [1,7,6,42,8,56]  case for differentiation.
c = [1,2,3,4,5] 
l = len(c)
rh_array = np.zeros((l,int(np.ceil(l/2))+1))

for j in range(l):
    if (j%2 == 0):
        rh_array[0][int(j/2)] = c[j]
    else:
        rh_array[1][int(j/2)] = c[j]



for r in range(2,l):


    if (rh_array[r - 1][0] == 0):
        if (np.all(rh_array[r - 1][:]) == 0):
            for z in range(int(l / 2)):
                if ((l - r + 1 - (2 * z)) >= 0):
                    rh_array[r - 1][z] = rh_array[r - 2][z] * ((l - r + 1 - (2 * z)))
                elif ((l - r + 1 - (2 * z)) < 0):
                    rh_array[r - 1][z] = 0

        else:
            rh_array[r - 1][0] = 0.000001

    for c in range(int(np.ceil(l/2))):



        rh_array[r][c] = ((rh_array[r-1][0]*rh_array[r-2][c+1]) - (rh_array[r-2][0]*rh_array[r-1][c+1]))/(rh_array[r-1][0])
print(rh_array)

def sign_changes(a):
    count = 0
    for r in range(a.shape[0] - 1):
        if (a[r][0]*a[r+1][0] < 0 ):
            count +=1
    return count
#print(sign_changes(rh_array))

print('There are %d roots on the right hand side of the complex plane'%(sign_changes(rh_array)))
