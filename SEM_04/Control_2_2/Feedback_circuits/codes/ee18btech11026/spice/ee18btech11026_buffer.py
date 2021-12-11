

import numpy as np
import matplotlib.pyplot as plt


#if using termux
import subprocess
import shlex
#end if

data=np.loadtxt('ee18btech11026_buffer.dat')
plt.plot(data[:,0],data[:,1])
plt.grid()
plt.xlabel("time")
plt.ylabel("Step response")
plt.title('Spice simulation for uncompensated system')

#if using termux




plt.savefig('./figs/ee18btech11026/ee18btech11026_spice_result_buffer.pdf')
plt.savefig('./figs/ee18btech11026/ee18btech11026_spice_result_buffer.eps')
subprocess.run(shlex.split("termux-open ./figs/ee18btech11026/ee18btech11026_spice_result_buffer.pdf"))
#else
#plt.show()
