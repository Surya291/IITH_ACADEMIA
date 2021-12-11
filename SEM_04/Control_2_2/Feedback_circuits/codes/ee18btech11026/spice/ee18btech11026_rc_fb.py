

import numpy as np
import matplotlib.pyplot as plt


#if using termux
import subprocess
import shlex
#end if

data=np.loadtxt('ee18btech11026_rc_fb.dat')
plt.plot(data[:,0],data[:,1])

plt.grid()
plt.xlabel("time")
plt.ylabel("Step response")
plt.title('Spice simulation for Compensated system')


plt.savefig('./figs/ee18btech11026/ee18btech11026_spice_result_rc_bf.pdf')
plt.savefig('./figs/ee18btech11026/ee18btech11026_spice_result_rc_bf.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_spice_result_rc_bf.pdf"))
#else
#plt.show()


plt.plot(data[70:121,0],data[70:121,1])

plt.grid()
plt.xlabel("time")
plt.ylabel("Step response")
y = np.arange(-2,14)
plt.yticks(y)
plt.title('Steady state Response (Magnified)')


plt.savefig('./figs/ee18btech11026/ee18btech11026_spice_result_rc_bf_mag.pdf')
plt.savefig('./figs/ee18btech11026/ee18btech11026_spice_result_rc_bf_mag.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_spice_result_rc_bf_mag.pdf"))
#else
#plt.show()
