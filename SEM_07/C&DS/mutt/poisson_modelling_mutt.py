'''
This script iterates over the folder containing the cached emails . 
#### The experiment is done for the months of sept and august (61 days)

parses the time stamps into day-date-time. 

creates the time series  where each element describes the no. of emails \
recieved in a single hour. 

1. Later we try to model the random variable : K(no. of emails per hour)
as a poisson distribution.

2. We observe that K takes the value 0 more frequently.

3. Again try to model the distribution with a variant of poisson called 
ZIP distribution (Zero inflated Poisson)
'''

import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import math

from util import *

#######
# IMPORTANT : ENTER YOUR MUTT INBOX DIRECTORY BELOW !!!!
#######
inbox_direc = '/home/surya/.mutt/cache/bodies/imaps:ee18btech11026@iith.ac.in@imap.gmail.com:993/INBOX'

day = []
mon = []
year = []
hour = []
minute = []
sec = []

############################################
##    Creating a dataframe containing time stamps of each email
###########################################
for filename in os.listdir(inbox_direc):
    with open(os.path.join(inbox_direc, filename),"r") as f :
        data= f.read().splitlines()
        
        data = data[2][13:32]
        try : 
            d = datetime.strptime(data, "%d %b %Y  %H:%M:%S")
        except:
            continue
        day.append(d.day)
        mon.append(d.month)
        year.append(d.year)
        hour.append( (d.hour + 12)%24 ) 
        minute.append(d.minute)
        sec.append(d.second)

df = pd.DataFrame()
df['day'] = day
df['mon'] = mon
df['year'] = year
df['hour'] = hour
df['min'] = minute
df['sec'] = sec

#print(len(df))

### creating a col "count" denoting mails per hour...
mails_per_hour = df.groupby(['day','mon', 'hour']).size().sort_values(ascending=False).reset_index(name='count') 
#print(mails_per_hour)


################  Creating time series data .... 

### Enter month no. from which mails are to be considered
mon_no = 8 ### August

mails_per_hour["hr_index"] = (mails_per_hour["mon"]-mon_no)*31*24 + (mails_per_hour["day"]-1)*24 + mails_per_hour["hour"]
mails_per_hour = mails_per_hour.loc[ (mails_per_hour['hr_index'] >= 0 )] ### ignoring july emails
#print(np.amax(mails_per_hour['hr_index']) )

#### Creating the time series 
time_series_h = np.zeros(np.amax(mails_per_hour['hr_index']) + 1)
for _, row in mails_per_hour.iterrows():
    time_series_h[row['hr_index']] = row['count']


plt.bar(np.arange(len(time_series_h)), time_series_h, color = 'blue')
plt.title("Time series data of mails received in the months \nof Aug & Sept")
plt.xlabel("hour index")
plt.ylabel("No. of emails received in an hour")
plt.savefig('time_series.svg')
plt.plot()
plt.show()



###############################################################
#######  Poisson modelling ......
#################################################################
a = np.arange(24) ## consider all hours 
hr_dict, lam1 = find_mean_of_all_hrs(mails_per_hour, mon_no,  x = a)

## poisson 
x = np.sort(  list(hr_dict.keys()).copy())
f1 = poisson_pmf(x, lam1)


###############################################################
#######  ZIP modelling ......
#################################################################
m = np.mean(time_series_h)
var = np.var(time_series_h)

## finding model estimates
_lam = ((var + (m**2) )/m) - 1
_pi = (var - m)/(var + (m**2) -m )
f2 = zero_poisson_pmf(x, _lam, _pi)


plt.bar(list(hr_dict.keys()), list(hr_dict.values()), color = 'blue', label = 'Data statistics') 
plt.plot(x,f1,color = 'green', label= 'Poisson approximation' )
plt.plot(x,f2, color = 'red', label= 'ZIP approximation')
plt.title("Modelling as a ZIP distribution (lam_z = %.2f, pi_z = %.2f) \n Vs Poisson distribution (lam = %.2f) "%(_lam,_pi, lam1))
plt.xlabel('k : mails received per hour')
plt.ylabel(' pmf (k)')
plt.legend()
plt.savefig('poisson.svg')
plt.plot()
plt.show()