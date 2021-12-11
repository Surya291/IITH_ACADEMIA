import pandas  as pd 
import matplotlib.pyplot as plt 
import numpy as np

df = pd.read_csv('/home/surya/Desktop/SEM_07/SmartGrid/data logger - K45.csv')


#str_idx,end_idx =1346, len(df)

str_idx,end_idx =1397, len(df)


idx_list = np.arange(str_idx,end_idx)


new_df = df.iloc[idx_list]
new_df = new_df.dropna()

#print(new_df.head())

time_list = np.arange(len(new_df))

v_list = list(new_df['Voltage (V)'])
i_list = list(new_df['Current (A)'])
p_list = list(new_df['Power (W)'])
pf_list = list(new_df['Power Factor'])
e_list = list(new_df['Energy (kwh)'])


plt.plot(time_list, v_list)
plt.xlabel('time')
plt.ylabel('Voltage(V)')
plt.title('V vs time')
plt.savefig('images/V.png')
plt.show()


plt.plot(time_list, i_list)
plt.xlabel('time')
plt.ylabel('current(I) in Amps')
plt.title('I vs time')
plt.savefig('images/I.png')
plt.show()


plt.plot(time_list, p_list)
plt.xlabel('time')
plt.ylabel('Power in Watt')
plt.title('P vs time')
plt.savefig('images/P.png')
plt.show()


plt.plot(time_list, e_list)
plt.xlabel('time')
plt.ylabel('Energy(kWh)')
plt.title('energy consumed vs time')
plt.savefig('images/E.png')
plt.show()

