import matplotlib.pyplot as plt
import math
import os



n_val = []
log_time = []
log_val = []
c = 6e-7
d = 2e-7
f = open('logn_runtimes.txt','r')
for row in f:
    row = row.split(',')
    n_val.append(int(row[0]))
    log_time.append(float(row[1]))
    log_val.append(float(c*math.log(int(row[0]),10) + d))


plt.figure(figsize=(8, 6), dpi=200)
plt.plot(n_val[:], log_time, color = 'r', label='runtime(w.r.t n)')
plt.plot(n_val, log_val, color = 'b', label = 'y = clog(n)')

plt.xscale("log")
plt.xlabel('n : no. of elements')
plt.ylabel('run time (in sec)')
plt.title('Worst Case Time Complexity wrt n while k is constant')

plt.legend()
plt.savefig('logn.eps', format='eps')
plt.show()
####################################################################


k_val = []
k_time = []
y_k = []
c = 0.85e-8
f2 = open('k_runtimes.txt','r')
for row in f2:
    row = row.split(',')
    k_val.append(float(row[0]))
    k_time.append(float(row[1]))
    y_k.append(float(row[0])*c)

plt.figure(figsize=(8, 6), dpi=200)
plt.plot(k_val, k_time, color = 'r', label='runtime(w.r.t k)')
plt.plot(k_val, y_k, color = 'b', label='y = c*k')
plt.xlabel('k : no. of elements in the range')
plt.ylabel('run time (in sec)')
plt.title('Worst Case Time Complexity wrt k while n = 1e4')

plt.legend()
plt.savefig('k.eps', format='eps')
plt.show()
