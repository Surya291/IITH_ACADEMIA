
import numpy as np
from matplotlib import pyplot as plt
import math
import scipy.fftpack
Pic = np.load('../../.PyCharmCE2019.3/config/scratches/binary_image.npy')
#plt.imshow(MonaLisa,'gray'), plt.show()

# converts to 1D array.
def convertto1D(MonaLisa):
    m = []
    for i in MonaLisa:
        for j in i:
            m.append(j)
    return m
pixels = convertto1D(Pic)
print(np.shape(Pic))

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

s = transmitted_signal(pixels)

#Adding Noise.......
def adding_channel_noise(s,N_0):
    w = np.random.normal(0, np.sqrt(N_0 / 2), 275000)
    r = s+w
    return r

#Calculating energy per bit........
def E_b(s) :
    e_avg = np.square(s).mean()
    E_b = e_avg/2
    return E_b

E_b = E_b(s)

#Calculating N_0
dB = 5
N_0 = (E_b/(10**(dB/10)))


r = adding_channel_noise(s,0.15811)

"""
#Signal strength..
total_energy = 0
for e in (r) :
    total_energy += (e)**2
e_avg = (total_energy) /(len(r))
print(e_avg)
"""


#Demodulation
def demodulation(r):
    a = np.zeros(50)
    b = np.zeros(50)
    f_c = np.int(2 * (1e6))
    f_s = np.int(50 * (1e6))
    t_s = 1 / f_s
    for k in range(1,2):
        for j in range(50):
            a[j] = (r[(k+1)*j]* np.cos(2*(np.pi)*f_c*((k+1)*j)*t_s))
            b[j] = (r[(k+1)*j]* np.sin(2*(np.pi)*f_c*((k+1)*j)*t_s))
        af = scipy.fftpack.fft(a)
        bf = scipy.fftpack.fft(b)
        xf = np.linspace(0.0, 1.0 / (1.0 * t_s), 50)
        #plt.plot(xf,af)
        plt.plot(xf,bf)
        plt.show()
        print(bf[0])
    return

demodulation(r)