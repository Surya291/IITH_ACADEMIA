import numpy as np
from matplotlib import pyplot as plt
import math
import scipy.fftpack
Pic = np.load('binary_image.npy')
#plt.imshow(Pic,'gray'), plt.show()

# converts to 1D array.
def convertto1D(MonaLisa):
    m = []
    for i in MonaLisa:
        for j in i:
            m.append(j)
    return m


#Getting symbols from 1D array
def converting_pixels_to_coordinates(pixels):
    x = np.zeros(len(pixels))
    for p in range(len(x)) :
        if (pixels[p] == 0):
            x[p] = 1
        else:
            x[p] = -1
    return x

#Modulating the symbols
def transmitted_signal(pixels) :
    x = converting_pixels_to_coordinates(pixels)
    f_c = np.int(2*(1e6))
    f_s = np.int(50*(1e6))
    t_s = 1/f_s
    s = np.zeros(275000)

    for n in range(len(s)) :
        s[n] = (x[np.int(2*(math.floor(n/50)))] * np.cos(2*(np.pi)*f_c*(n)*t_s)) + (x[np.int((2*(math.floor(n/50)))+1)] * np.sin(2*(np.pi)*f_c*(n)*t_s))
    return s



#Adding Noise.......
def adding_channel_noise(s,N_0):
    f_s = 50*(1e6)
    w = np.random.normal(0, np.sqrt((N_0) / 2), 275000)
    r = s
    return r

#Calculating energy per bit........
def E_b(s) :
    e_avg = np.square(s).mean()
    e_avg = e_avg * 50
    E_b = e_avg/2
    return E_b



#Calculating N_0
def calculating_N_0(dB,E_b):
    N_0 = (E_b/(10**(dB/10)))
    return N_0


"""
#Signal strength..
total_energy = 0
for e in (r) :
    total_energy += (e)**2
e_avg = (total_energy) /(len(r))
print(e_avg)
"""

def Ideal_signals(a,b,t):
    f_c = np.int(2 * (1e6))
    f_s = np.int(50 * (1e6))
    t_s = 1 / f_s
    s = np.zeros(50)
    for n in range(len(s)) :
        s[n] = (a * np.cos(2*(np.pi)*f_c*(50*t + n)*t_s)) + (b * np.sin(2*(np.pi)*f_c*(50*t + n)*t_s*t))
    return s


def Cal_mse(a,b):
    sum = 0
    for e in range(50):
        sum = ((a[e] - b[e])**2) + sum
    return (sum**0.5)


#Demodulation
def min_distance(r):
    sym = []
    a = np.zeros(50)
    b = np.zeros(50)
    f_c = np.int(2 * (1e6))
    f_s = np.int(50 * (1e6))
    t_s = 1 / f_s
    for k in range(5500):
        mse = []
        s1 = Ideal_signals(1, 1, k+1)
        s2 = Ideal_signals(1, -1, k+1)
        s3 = Ideal_signals(-1, 1, k+1)
        s4 = Ideal_signals(-1, -1, k+1)
        for j in range(50):
            a[j] = r[(k+1)*j]
        mse.append(Cal_mse(a, s1))
        mse.append(Cal_mse(a, s2))
        mse.append(Cal_mse(a, s3))
        mse.append(Cal_mse(a, s4))

        """mse.append(((a - s1) ** 2).mean(axis=0))
        mse.append(((a - s2) ** 2).mean(axis=0))
        mse.append(((a - s3) ** 2).mean(axis=0))
        mse.append(((a - s4) ** 2).mean(axis=0))"""
        print(mse)
        sym.append(mse.index(min(mse)))
    return sym



def getting_1D_mona(sym):
    mona = np.zeros(11000)
    for i in range(5500):
        if(sym[i] == 0):
            mona[(2*i)] = 0
            mona[(2*i)+1] = 0

        elif (sym[i] == 1):
            mona[(2 * i)] = 0
            mona[(2 * i) + 1] = 1

        elif (sym[i] == 2):
            mona[(2 * i)] = 1
            mona[(2 * i) + 1] = 0

        elif (sym[i] == 3):
            mona[(2 * i)] = 1
            mona[(2 * i) + 1] = 1
    return mona

def monali(mona):
    monal = np.reshape(mona,(110,100))
    return monal


pixels = convertto1D(Pic)
s = transmitted_signal(pixels)
E_b = E_b(s)

N_0 = calculating_N_0(10, 25)
r = adding_channel_noise(s,N_0)
sym = min_distance(r)
print(sym)
print(s[274999])
mona = getting_1D_mona(sym)
monal = monali(mona)
plt.imshow(monal,'gray'), plt.show()