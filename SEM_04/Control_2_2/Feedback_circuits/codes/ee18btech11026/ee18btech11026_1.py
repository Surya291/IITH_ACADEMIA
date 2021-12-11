
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math
#if using termux
import subprocess
import shlex
#endif


pi = math.pi

p1 = 2*pi*1e6
p2 = 2*pi*1e7
p3 = 2*pi*1e8
pD = 2*pi*1e2

#Uncompensated Loop Gain
s1 = signal.lti([],[-p1,-p2,-p3],1e4*p1*p2*p3)
#Compensated Loop Gain
s2 = signal.lti([],[-p1,-p2,-p3,-pD],1e4*p1*p2*p3*pD)

w1,mag1,phase1 = signal.bode(s1,n = 1000)
w2,mag2,phase2 = signal.bode(s2,n = 1000)
zero = np.zeros(len(w2))


fig1,a = plt.subplots(2)

a[0].set_xlabel('Freq (in rad/s)')
a[0].set_ylabel('Mag (in dB)')
a[0].set_title('Magnitude plot ')
a[0].semilogx(w1,mag1,label = 'Uncompensated : $L_{1}(s)$')
a[0].semilogx(w2,mag2,label = 'Compensated : $L_{2}(s)$')
a[0].scatter(2.36e8,35)
a[0].annotate("$w_{1} : > 0dB$",(3.5e8,35))
a[0].scatter(1.89e7,-20)
a[0].annotate("$w_{2}: < 0dB $",(2.5e7,-20))

a[0].semilogx(w2,zero)


a[0].legend()
a[0].grid()

a[1].set_xlabel('Freq (in rad/s)')
a[1].set_ylabel('Phase (in deg)')
a[1].set_title('Phase plot ')
a[1].semilogx(w1,phase1,label = 'Uncompensated:$L_{1}(s)$')
a[1].semilogx(w2,phase2,label = 'Compensated:$L_{2}(s)$')
a[1].scatter(2.36e8,-180)
a[1].annotate("$w_{1}$",(3.5e8,-180))
a[1].scatter(1.89e7,-180)
a[1].annotate("$w_{2}$",(2.5e7,-180))
a[1].set_yticks(np.arange(0,-360,-90))
a[1].legend()
a[1].grid()

#if using termux
fig1.savefig('./figs/ee18btech11026/ee18btech11026_2.pdf')
fig1.savefig('./figs/ee18btech11026/ee18btech11026_2.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_2.pdf"))


#plt.show()




# Asymptotic bode plots.

Slopes = np.array([0,0,0,0,0,0,-20,-40,-60])
Slopes2 = np.array([0,0,-20,-20,-20,-20,-40,-60,-80])
x = np.array([1,10,100,1000,10000,1e5,1e6,1e7,1e8,1e9])
y3 = np.zeros(len(x))
y = []
y2 = []
k = 80
k2 = 80
for i in range(len(x) - 1):
    y.append(k)
    y2.append(k2)
    k += Slopes[i]
    k2 += Slopes2[i]
y.append(k)
y2.append(k2)
plt.semilogx(x, y)
plt.semilogx(x,y2)
plt.semilogx(x,y3)
plt.grid()
#plt.xticks(np.arange(min(x), max(x)+1))
plt.xticks(x)
plt.yticks(np.arange(80,-180,-40))
plt.xlabel('Frequency(Hz)')
plt.ylabel('Gain in dB')
plt.legend(['Uncompensated : G(s)', 'Compensated : G(s)H(s)','0 dB line'])
plt.text(1e2-40,-230,'$f_{D}$',color = 'r',fontsize = 16)
plt.text(1e6-4e5,-230,'$f_{p1}$',color = 'r',fontsize = 16)
plt.text(1e7-4e6,-230,'$f_{p2}$',color = 'r',fontsize = 16)
plt.text(1e8-4e7,-230,'$f_{p3}$',color = 'r',fontsize = 16)
y = [80,0]
x = [1e2,1e6]
plt.vlines(x, -180, y, linestyle="dashed")


#if using termux
plt.savefig('./figs/ee18btech11026/ee18btech11026_1.pdf')
plt.savefig('./figs/ee18btech11026/ee18btech11026_1.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_1.pdf"))



#else
#plt.show()

