"""Vedala Sai Ashok and Koidala Surya Prakash"""

#EE18BTECH11044
#EE18BTECH11026


import numpy as np
from matplotlib import pyplot as plt
import math

# converts into 1D array.
def convertto1D(MonaLisa):
    m = []
    for i in MonaLisa:
        for j in i:
            m.append(j)
    return m
#print(convertto1D(Pic))

#converting into symbols..
def converting_pixels_to_coordinates(pixels):
    x = np.zeros(len(pixels))
    for i in range(len(pixels)):
        if (pixels[i] == 0):
            x[i] = 1
        elif(pixels[i] == 1):
            x[i] = -1
    return x



#Modulating signals..
def transmitted_signal(x) :
    f_c = np.int(2*(1e6))
    f_s = np.int(50*(1e6))
    t_s = 1/f_s
    s = np.zeros(275000*2)

    count = 0
    for n in range(len(s)) :
        count+=1
        #print(count)
        s[n] = (x[np.int(2*(math.floor(n/50)))] * np.cos(2*(np.pi)*f_c*(n)*t_s)) + (x[np.int((2*(math.floor(n/50)))+1)] * np.sin(2*(np.pi)*f_c*(n)*t_s))
    
    return s

#print(s[50:100])
#print(x)

#Adding noise..
def adding_noise(N_0,s) :
    f_s = 50000000
    #w = np.random.normal(0, np.sqrt((N_0) / 2), 275000)
    w = np.random.normal(0, np.sqrt((N_0 * f_s) / 2), 275000*2)
    s = s + w
    return s



#Calculating energy per bit........
def E_b(s):
#We are calculating the energy of input signal for 1 micro second
# which corresponds to two bits.    
    return 0.0000005



#Calculating N_0
def calculating_N_0(dB,E_b):
    N_0 = (E_b/(10**(dB/10)))
    return N_0



#Ideal Signals..
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

#Mean_square_error
def mse(a,b):
    sum = 0
    for e in range(50):
        sum = ((a[e] - b[e])**2) + sum
    return (sum**0.5)


#demodulation
def min_dist(r):
    sym = []
    a = np.zeros(50)
    b = np.zeros(50)
    f_c = np.int(2 * (1e6))
    f_s = np.int(50 * (1e6))
    t_s = 1 / f_s

    for k in range(5500*2):
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
    mona = np.zeros(11000*2)
    for i in range(5500*2):
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

#Bit Error Rate
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


def encodingch13(a,z):
    l = len(a)
    w = int(l/4)
    d8 = np.zeros(8)
    d12 = np.zeros(12)
    #defining the matrix
    g1 = np.zeros((4,8))
    ##
    g1[0][0] = 1
    g1[0][1] = 1
    g1[0][2] = 1
    g1[0][3] = 1
    g1[0][4] = 0
    g1[0][5] = 0
    g1[0][6] = 0
    g1[0][7] = 0
    ##
    g1[1][0] = 1
    g1[1][1] = 1
    g1[1][2] = 0
    g1[1][3] = 0
    g1[1][4] = 1
    g1[1][5] = 1
    g1[1][6] = 0
    g1[1][7] = 0
    ##
    g1[2][0] = 1
    g1[2][1] = 0
    g1[2][2] = 1
    g1[2][3] = 0
    g1[2][4] = 1
    g1[2][5] = 0
    g1[2][6] = 1
    g1[2][7] = 0
    ##
    g1[3][0] = 0
    g1[3][1] = 1
    g1[3][2] = 1
    g1[3][3] = 0
    g1[3][4] = 1
    g1[3][5] = 0
    g1[3][6] = 0
    g1[3][7] = 1

    g2 = np.zeros((4,12))
    ##
    g2[0][0] = 1
    g2[0][1] = 0
    g2[0][2] = 0
    g2[0][3] = 0
    g2[0][4] = 0
    g2[0][5] = 1
    g2[0][6] = 1
    g2[0][7] = 1
    g2[0][8] = 1
    g2[0][9] = 0
    g2[0][10] = 1
    g2[0][11] = 0
    ##
    g2[1][0] = 0
    g2[1][1] = 1
    g2[1][2] = 0
    g2[1][3] = 0
    g2[1][4] = 1
    g2[1][5] = 0
    g2[1][6] = 1
    g2[1][7] = 1
    g2[1][8] = 0
    g2[1][9] = 1
    g2[1][10] = 1
    g2[1][11] = 0
    ##
    g2[2][0] = 0
    g2[2][1] = 0
    g2[2][2] = 1
    g2[2][3] = 0
    g2[2][4] = 1
    g2[2][5] = 1
    g2[2][6] = 1
    g2[2][7] = 0
    g2[2][8] = 1
    g2[2][9] = 1
    g2[2][10] = 1
    g2[2][11] = 1
    ##
    g2[3][0] = 0
    g2[3][1] = 0
    g2[3][2] = 0
    g2[3][3] = 1
    g2[3][4] = 0
    g2[3][5] = 0
    g2[3][6] = 0
    g2[3][7] = 1
    g2[3][8] = 1
    g2[3][9] = 1
    g2[3][10] = 1
    g2[3][11] = 1

    
    c1 = np.zeros(4)
    c2 = np.zeros(4)
    c11 = np.zeros(8)
    c21 = np.zeros(8)
    d1 = []
    d2 = []
    d3 = []

    for i in range(2):
        for j in range(2):
            for k in range(2):
                for t in range(2):
                    c1[0] = i
                    c1[1] = j
                    c1[2] = k
                    c1[3] = t
                    c11 = np.matmul(g1.T,c1)
                    for p in range(8):
                        c11[p] = c11[p]%2
                        d1.append(c11[p])

                        
    for i in range(2):
        for j in range(2):
            for k in range(2):
                for t in range(2):
                    c2[0] = i
                    c2[1] = j
                    c2[2] = k
                    c2[3] = t
                    c21 = np.matmul(g2.T,c2)
                    for q in range(12):
                        c21[q] = c21[q]%2
                        d2.append(c21[q])


    for i in range(2):
        for j in range(2):
            for k in range(2):
                for t in range(2):
                    d3.append(i)
                    d3.append(j)
                    d3.append(k)
                    d3.append(t)
                    
                    



    arr1 = np.zeros(8*w)
    arr2 = np.zeros(12*w)
    
    for i in range(0,w):
        if(z == 8):
            
            """
            b[0] = a[4*i]
            b[1] = a[np.int(4*i)+1]
            b[2] = a[np.int(4*i)+2]
            b[3] = a[np.int(4*i)+3]
            """
            d8 = np.matmul(g1.T,a[4*i:(4*i)+4])

            for j in range(z):
                d8[j] = d8[j]%2
        arr1[8*i:(8*i)+8] = d8
            
            

        if(z == 12):
            b[0] = a[np.int(4*i)]
            b[1] = a[np.int(4*i)+1]
            b[2] = a[np.int(4*i)+2]
            b[3] = a[np.int(4*i)+3]
            d12 = np.matmul(g2.T,b)

            for k in range(z):
                d12[k] = d12[k]%2
                arr.append(d12[k])
                
    return arr1,d1,d2,d3

def chdecoding(a,d,z,d3):
    darr = []
    l = len(a)
    u = int(l/z)
    if(z == 8):
        b = np.zeros(8)
        l1 = len(d)
        v = int(l1/8)
        for i in range(u):
            b[0] = a[np.int(8*i)]
            b[1] = a[np.int(8*i)+1]
            b[2] = a[np.int(8*i)+2]
            b[3] = a[np.int(8*i)+3]
            b[4] = a[np.int(8*i)+4]
            b[5] = a[np.int(8*i)+5]
            b[6] = a[np.int(8*i)+6]
            b[7] = a[np.int(8*i)+7]
            mind = 0
            bit = 0
            for j in range(v):
                test = d[j*8:((j*8)+8)]
                s = 0
                for k in range(8):
                    s = s + abs((b[k] - test[k]))
                if((mind == 0) or (mind >= s)):
                    mind = s
                    bit = j
            arr1 = d3[bit*4:((bit*4)+4)]
            darr.append(arr1[0])
            darr.append(arr1[1])
            darr.append(arr1[2])
            darr.append(arr1[3])
    return darr



Pic = np.load('binary_image.npy')
pixels = convertto1D(Pic)
x1,d1,d2,d3 = encodingch13(pixels,8)
x = converting_pixels_to_coordinates(x1)
s = transmitted_signal(x)
E_b = E_b(s)
dB = 10
N_0 = calculating_N_0(dB,E_b)
r = adding_noise(N_0,s)
sym = min_dist(r)
mona = getting_1D_mona(sym)
mona11 = chdecoding(mona,d1,8,d3)
monal = monali(mona11)
print(monal)
ber = BER(pixels, mona)
print(ber)
plt.imshow(monal,'gray')
plt.title("SNR is 5dB")
plt.show()
