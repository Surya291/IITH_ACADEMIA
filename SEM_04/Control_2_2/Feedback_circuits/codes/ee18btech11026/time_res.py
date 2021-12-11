
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import math
from scipy.signal import  lsim
# Import the bellow Libraries if running on Termux
import subprocess
import shlex


pi = math.pi

p1 = 2*pi*1e6
p2 = 2*pi*1e7
p3 = 2*pi*1e8
pD = 2*pi*1e2


# constants
a4 = 1
a3 = p1+p2+p3+pD
a2 = (p1*p2) +(p1*p3)+(p1*pD)+(p2*p3)+(p2*pD)+(p3*pD)
a1 = (p1*p2*p3)+(p1*p2*pD)+(p1*pD*p3)+(pD*p2*p3)
a0 = p1*p2*p3*pD

g = 10**4
s3 = signal.lti([g*p1*p2*p3,g*a0],[a4,a3,a2,a1,(g+1)*a0])

f = 1e5 # enter the frequency
t_s = 1/f
t = np.linspace(0,25*t_s,5000)
u = np.sin(2*pi*f*t)
T,Y,X = lsim(s3,u,t)

w3, mag3, phase3 = s3.bode()
plt.semilogx(w3/(2*pi), mag3)
x = np.array([1,10,100,1000,10000,1e5,1e6,1e7,1e8,1e9])
plt.xticks(x)
plt.xlabel('Frequency (Hz)')
plt.ylabel('$20\log|T(f)|$')
plt.grid()
plt.savefig('../../figs/ee18btech11026/Bodeplot.eps')
plt.savefig('../../figs/ee18btech11026/Bodeplot.pdf')
#plt.show()


plt.plot(T,Y)
plt.title('f = '+str(f))

plt.savefig('../../figs/ee18btech11026/sinusoid_res.eps')
plt.savefig('../../figs/ee18btech11026/sinusoid_res.pdf')
#plt.show()
''' If using Termux '''
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/sinusoid_res.pdf"))
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/Bodeplot.pdf"))

