# Released under GNU-GPL
# By K.Surya Prakash
# Dt.28th Apr

# Released under GNU-GPL
# By K.Surya Prakash
# Dt.28th Apr

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import  step
#if using termux
import subprocess
import shlex
#endif

# open loop T.F's
s1 = signal.lti([1000], [1, 25,100,0])# G(s)
s5 = signal.lti([-3.115],[0,-5,-20,-50.24],1000*16.13)#G_c(s)*G(s)
s4 = signal.lti([-3.115],[-50.24],16.13)#G_c(s)

# Closed loop T.F's
s2 = signal.lti([1000], [1, 25,100,1000])#uncompensated
s3 = signal.lti([16130,16130*3.115], [1,75.24,1356,21154,16130*3.115])#compensated

w1,mag1,phase1 = signal.bode(s1,n = 1000)
w2,mag2,phase2 = signal.bode(s5,n = 1000)
w3,mag3,phase3 = signal.bode(s4,n = 1000)

fig1,a = plt.subplots(2)

a[0].set_xlabel('Freq (in rad/s)')
a[0].set_ylabel('Mag (in dB)')
a[0].set_title('Magnitude plot ')
a[0].semilogx(w1,mag1,label = 'Uncompensated')
a[0].scatter(12.48,-12.07)
a[0].annotate("$(w_{max}$,-12.07dB)",(14,-13))
a[0].legend()
a[0].grid()

a[1].set_xlabel('Freq (in rad/s)')
a[1].set_ylabel('Phase (in deg)')
a[1].set_title('Phase plot ')
a[1].semilogx(w1,phase1,label = 'Uncompensated')
a[1].legend()
a[1].grid()

#if using termux
fig1.savefig('./figs/ee18btech11026/ee18btech11026_1.pdf')
fig1.savefig('./figs/ee18btech11026/ee18btech11026_1.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_1.pdf"))



fig2,b = plt.subplots(2)

b[0].set_xlabel('Freq (in rad/s)')
b[0].set_ylabel('Mag (in dB)')
b[0].set_title('Magnitude plot ')
b[0].semilogx(w1,mag1,label = 'Uncompensated')
b[0].semilogx(w2,mag2,label = 'Compensated')
b[0].semilogx(w3,mag3,label = 'Compensator')
b[0].legend()
b[0].grid()


b[1].set_xlabel('Freq (in rad/s)')
b[1].set_ylabel('Phase (in deg)')
b[1].set_title('Phase plot ')
b[1].semilogx(w1,phase1,label = 'Uncompensated')
b[1].semilogx(w2,phase2,label = 'Compensated')
b[1].semilogx(w3,phase3,label = ' Lead Compensator')
b[1].annotate('', (12.6,-190), (12.6,-127), arrowprops=dict(facecolor='red',arrowstyle='<|-|>',mutation_scale=15))
b[1].annotate('', (12.6,0), (12.6,63), arrowprops=dict(facecolor='red',arrowstyle='<|-|>',mutation_scale=15))
b[1].annotate("Gain in Phase",(14,-160))
b[1].annotate("$\phi_{max}$",(14,30))
b[1].legend()
b[1].grid()


#if using termux
fig2.savefig('./figs/ee18btech11026/ee18btech11026_2.pdf')
fig2.savefig('./figs/ee18btech11026/ee18btech11026_2.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_2.pdf"))





plt.figure()
t3, s3 = step(s3)
t2,s2 = step(s2)
plt.plot(t2,s2,label = "Uncompensated")
plt.plot(t3,s3,label = "Compensated")
plt.scatter(0.516,1.527)
plt.scatter(0.22,1.13)
plt.annotate("$T_{p}$ = 0.5",(0.7,1.5))
plt.annotate("$T_{p}$ = 0.22",(0.4,1.1))
plt.title("Time responses")
plt.grid()
plt.legend()
# if using termux
plt.savefig('./figs/ee18btech11026/ee18btech11026_time.pdf')
plt.savefig('./figs/ee18btech11026/ee18btech11026_time.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_time.pdf"))



#else
#plt.show()



