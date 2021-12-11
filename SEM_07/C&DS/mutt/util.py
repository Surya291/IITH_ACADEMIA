'''
This scripts consists of set of functions used in poisson_modelling_mutt.py
'''
import numpy as np
import math
############ Modelling a zero inflated poisson distrivution
def zero_poisson_pmf(x_list, lam, pi): ### lam, pi are param
    ans = []
    for x in x_list:
        
        if(x == 0):
            y = pi + ( (1-pi)*(np.exp(-1*lam)*pow(lam,x)/(math.factorial(x)) ) )
        else:
            y = (1-pi)*(np.exp(-1*lam)*pow(lam,x)/(math.factorial(x)) )
        ans.append(y)
    return ans


############# Modelling a poisson distribution (generic variant)

def poisson_pmf(x_list, lam): ### lam := param
    ans = []
    for x in x_list:
        y = np.exp(-1*lam)*pow(lam,x)/(math.factorial(x))
        ans.append(y)
    return ans


def find_mean_of_all_hrs(mails_per_hour,mon_no,  x = [10,11]):
    '''
    mails_per_hour --> dataframe
    x: the set of hours to be considered [10,11]: only mails in 10 and 11 are considered
    mon_no : 8 : Above august all are considered 
    '''

    working_hrs = mails_per_hour.loc[ (mails_per_hour['mon'] >=mon_no ) & mails_per_hour['hour'].isin(x)  ]

    #datapoints = len(temp)
    hr_dict = {0: 61*(len(x)) - len(working_hrs)}
    for i in working_hrs['count']:
        if(i in hr_dict):
            hr_dict[i] = hr_dict[i] + 1
        else :
            hr_dict[i] = 1
               
    mean, total = 0, 61*len(x)
    for mails_no,cnt in hr_dict.items():
        mean = mean + mails_no*cnt
        hr_dict[mails_no] = hr_dict[mails_no]/total 
        
    return hr_dict, (mean/total)