"""Vedala Sai Ashok and Koidala Surya Prakash"""

#EE18BTECH11044
#EE18BTECH11026


import numpy as np
from matplotlib import pyplot as plt
import math

################################# converts into 1D array.
def convertto1D(MonaLisa):
    m = []
    for i in MonaLisa:
        for j in i:
            m.append(j)
    return m
#print(convertto1D(Pic))

################################# converting into symbols..
def converting_pixels_to_coordinates(pixels):
    x = np.zeros(len(pixels))
    for i in range(len(pixels)):
        if (pixels[i] == 0):
            x[i] = 1
        elif(pixels[i] == 1):
            x[i] = -1
    return x

#print(len(x))
##################################### Modulating signals..
def transmitted_signal(x) :
    f_c = np.int(2*(1e6))
    f_s = np.int(50*(1e6))
    t_s = 1/f_s
    s = np.zeros(3*60000*50)


    for n in range(len(s)) :
        s[n] = (x[np.int(2*(math.floor(n/50)))] * np.cos(2*(np.pi)*f_c*(n)*t_s)) + (x[np.int((2*(math.floor(n/50)))+1)] * np.sin(2*(np.pi)*f_c*(n)*t_s))
    return s

#print(s[50:100])
#print(x)
##################################### Adding noise..
def adding_noise(N_0,s) :
    f_s = 50000000
    w = np.random.normal(0, np.sqrt((N_0*f_s) / 2),3*60000*50)
    #w = np.random.normal(0, np.sqrt(5), 3*60000*50)
    s = s + w
    return s



############################Calculating energy per bit........
def E_b(s):
#We are calculating the energy of input signal for 1 micro second
# which corresponds to two bits.    
    return 0.0000005*3



###########################Calculating N_0
def calculating_N_0(dB,E_b):
    N_0 = (E_b/(10**(dB/10)))
    return N_0



##################################### Ideal Signals..
def Ideal_signals(a,b,k):
    f_c = np.int(2*(1e6))
    f_s = np.int(50*(1e6))
    t_s = 1/f_s

    s = np.zeros(50)
    for n in range(len(s)):
        s[n] = a*(np.cos(2*(np.pi)*f_c*(50*(k) + n)*t_s)) + b*(np.sin(2*(np.pi)*f_c*(50*(k) + n)*t_s))
    return s
#c1 = Ideal_signals(-1,-1,1)
'''c2 = Ideal_signals(1,-1)
c3 = Ideal_signals(-1,1)
c4 = Ideal_signals(-1,-1)'''

################################### Mean_square_error
def mse(a,b):
    sum = 0
    for e in range(50):
        sum = ((a[e] - b[e])**2) + sum
    return (sum**0.5)
#################################  Demodulation...
def min_dist(r):
    sym = []
    a = np.zeros(50)
    b = np.zeros(50)
    f_c = np.int(2 * (1e6))
    f_s = np.int(50 * (1e6))
    t_s = 1 / f_s

    for k in range(3*60000):
        l = []
        s1 = Ideal_signals(1, 1, k)
        s2 = Ideal_signals(1, -1, k)
        s3 = Ideal_signals(-1, 1, k)
        s4 = Ideal_signals(-1, -1, k)
        a = r[(50*k):((50*k) + 50)]

        l.append(mse(a,s1))
        l.append( mse(a, s2))
        l.append(mse(a, s3))
        l.append(mse(a, s4))

        sym.append(l.index((min(l))))
    return sym

#print(p)

def getting_1D_mona(sym):
    mona = np.zeros(3*120000)
    for i in range(3*60000):
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

    monal = np.reshape(mona,(400,300))
    return monal

################################# Bit Error Rate
def Calc_mismatch(pixels, mona):
    count = 0
    for i in range(len(pixels)):
        if(pixels[i] != mona[i]):
            count = count+1
    return count


def BER(pixels, mona):
    count = 0
    for i in range(len(pixels)):
        if (pixels[i] != mona[i]):
            count = count + 1
    return (count/len(pixels))

def channel_encoding_2(pixels):
    encoding_ch2 = np.zeros(3*(len(pixels)))

    for i in range(len(pixels)):
        k = pixels[i]
        encoding_ch2[3*i] = k
        encoding_ch2[(3*i) + 1] = k
        encoding_ch2[(3*i) + 2] = k
    return encoding_ch2

def decoding_2(sym):
    decoded = np.zeros(len(pixels))
    for i in range(len(decoded)):
        count = 0
        for p in range(3*i , (3*i)+ 3):
            if (sym[p] == 0):
                count = count + 1
        if (count >=2):
            decoded[i] = 0
        else:
            decoded[i] = 1
    return decoded
Pic = np.load('mss.npy')
pixels = convertto1D(Pic)
x = converting_pixels_to_coordinates(pixels)
encoded = channel_encoding_2(x)
s = transmitted_signal(encoded)
E_b = E_b(s)
dB = 6
N_0 = calculating_N_0(dB,E_b)
r = adding_noise(N_0,s)
sym = min_dist(r)
#print(sym)
mona = getting_1D_mona(sym)
decoded = decoding_2(mona)
monal = monali(decoded)

#print(pixels)
#print(mona)
ber = BER(pixels, decoded)
count = Calc_mismatch(pixels, decoded)
print(ber)
print(ber*120000)
plt.imshow(monal,'gray')
plt.title("6dB for repetitive encoding")
#plt.imshow(Pic,'gray')
plt.show()
