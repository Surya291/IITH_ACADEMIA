import numpy as  np
import matplotlib.pyplot as plt

## for variance plot for 4 to 8
x3 = [20,12,7,5]
y3 = [0.0504 , 0.0112 , 0.0009 ,0.0001]


y2 = [0.047,0.0155,0.0024,0.00054]

y1 = [0.0899,0.03289,0.0061,0.00086]


plt.semilogy(x3,y3)

plt.xlabel('variance')
plt.ylabel('BER')
plt.title( 'BER vs variance for channel_encoder_3')
plt.savefig("/home/surya/Desktop/log_plots/var_3")
plt.show()

plt.semilogy(x3,y2)
plt.xlabel('variance')
plt.ylabel('BER')
plt.title( 'BER vs variance for channel_encoder_2')
plt.savefig("/home/surya/Desktop/log_plots/var_2")
plt.show()

plt.semilogy(x3,y1)
plt.xlabel('variance')
plt.ylabel('BER')
plt.title( 'BER vs variance for channel_encoder_1')
plt.savefig("/home/surya/Desktop/log_plots/var_1")
plt.show()

a = [-2,0,2,4,6]
b1 = [0.1903,0.1207,0.0597,0.0197,0.003]
b2 = [0.166,0.1117,0.06175,0.02045,0.0075]
b3 = [0.209,0.1356,0.07271,0.023991,0.00397]

plt.semilogy(a,b1)

plt.xlabel('E_b/N_0 values in dB')
plt.ylabel('BER')
plt.title( 'BER vs SNR for channel_encoder_1')
plt.savefig("/home/surya/Desktop/log_plots/snr_1")
plt.show()

plt.semilogy(a,b2)

plt.xlabel('E_b/N_0 values in dB')
plt.ylabel('BER')
plt.title( 'BER vs SNR for channel_encoder_2')
plt.savefig("/home/surya/Desktop/log_plots/snr_2")
plt.show()

plt.semilogy(a,b3)

plt.xlabel('E_b/N_0 values in dB')
plt.ylabel('BER')
plt.title( 'BER vs SNR for channel_encoder_3')
plt.savefig("/home/surya/Desktop/log_plots/snr_3")
plt.show()

