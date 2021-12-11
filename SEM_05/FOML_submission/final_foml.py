## imports here !!!
import numpy as np
import pandas as pd
import xgboost as xgb


from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

from sklearn.impute import SimpleImputer
import random
random.seed(10)





'''
Importing data
'''
train_data= pd.read_csv('iith_foml_2020_train.csv')
train = pd.DataFrame(train_data)
test_data= pd.read_csv('iith_foml_2020_test.csv')
test = pd.DataFrame(test_data)


def imputing_missing_values(df):
    data = df.to_numpy()
    # define the imputer
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer  = imputer.fit(data)
    # transform the dataset
    transformed_values = imputer.transform(data)
    imputed_data = pd.DataFrame(data = transformed_values,columns = df.columns) 
    return imputed_data


imputed_train = imputing_missing_values(train)
imputed_test = imputing_missing_values(test)




'''
Dividing into X, Y
'''
Y = imputed_train['Target Variable (Discrete)']
X = imputed_train.drop(columns=['Feature 2 (Discrete)','Feature 4 (Discrete)','Feature 9','Feature 20 (Discrete)', 'Feature 21 (Discrete)','Feature 22 (Discrete)','Feature 16', 'Feature 17','Target Variable (Discrete)'],axis = 1)
X_test = imputed_test.drop(columns=['Feature 2 (Discrete)','Feature 4 (Discrete)','Feature 9','Feature 20 (Discrete)', 'Feature 21 (Discrete)','Feature 22 (Discrete)','Feature 16', 'Feature 17'],axis = 1)
#################################################################################



'''
Training with stratified K-fold
'''

i=1
kf = StratifiedKFold(n_splits=10,random_state=1,shuffle=True)

param_grid = [{'min_child_weight': [2.0]}] #set of trial values for min_child_weight


for train_index,test_index in kf.split(X,Y):
    print('\n{} of kfold {}'.format(i,kf.n_splits))
    xtr,xvl = X.loc[train_index],X.loc[test_index]
    ytr,yvl = Y[train_index],Y[test_index]

    model =GridSearchCV(XGBClassifier(), param_grid, cv=10, scoring= 'f1_macro',iid=True)
    model.fit(xtr, ytr)

    #print (model.best_params_)
    y_pred=model.predict(xvl)
    y_pred = [round(value) for value in y_pred]
    
    
    #print('accuracy_score',accuracy_score(yvl,y_pred) * 100)
    i+=1

    
def predict_and_submission(test_data,model,title):### test_data in pd format
    test = pd.DataFrame(test_data)
    predictions = model.predict(test)

    output_test_data = pd.DataFrame() 
    output_test_data['Category'] = predictions.astype(int)

    output_test_data['Id'] = list(np.arange(1,predictions.size+1))

    submission = output_test_data[['Id','Category']]
    submission.to_csv(title, index=False)
    submission.head()
    return submission

##### Plsss change the title........
output = predict_and_submission(X_test,model,title = "Model_1.csv")

#######################################################################################################
#######################################################################################################
#######################################################################################################


## imports here !!!
import numpy as np
import pandas as pd
import xgboost as xgb


from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

from sklearn.impute import SimpleImputer
import random
random.seed(10)





'''
Importing data
'''
train_data= pd.read_csv('iith_foml_2020_train.csv')
train = pd.DataFrame(train_data)
test_data= pd.read_csv('iith_foml_2020_test.csv')
test = pd.DataFrame(test_data)


def imputing_missing_values(df):
    data = df.to_numpy()
    # define the imputer
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer  = imputer.fit(data)
    # transform the dataset
    transformed_values = imputer.transform(data)
    imputed_data = pd.DataFrame(data = transformed_values,columns = df.columns) 
    return imputed_data


imputed_train = imputing_missing_values(train)
imputed_test = imputing_missing_values(test)



'''
Dividing into X, Y
'''
Y = imputed_train['Target Variable (Discrete)']
X = imputed_train.drop(columns=['Feature 16', 'Feature 17','Target Variable (Discrete)'],axis = 1)
X_test = imputed_test.drop(columns=['Feature 16', 'Feature 17'],axis = 1)



'''
Training with stratified K-fold
'''

i=1
kf = StratifiedKFold(n_splits=10,random_state=1,shuffle=True)

param_grid = [{'min_child_weight': [2.0]}] #set of trial values for min_child_weight


for train_index,test_index in kf.split(X,Y):
    print('\n{} of kfold {}'.format(i,kf.n_splits))
    xtr,xvl = X.loc[train_index],X.loc[test_index]
    ytr,yvl = Y[train_index],Y[test_index]

    model =GridSearchCV(XGBClassifier(), param_grid, cv=10, scoring= 'f1_macro',iid=True)
    model.fit(xtr, ytr)

    #print (model.best_params_)
    y_pred=model.predict(xvl)
    y_pred = [round(value) for value in y_pred]
    
    
    #print('accuracy_score',accuracy_score(yvl,y_pred) * 100)
    i+=1

    
def predict_and_submission(test_data,model,title):### test_data in pd format
    test = pd.DataFrame(test_data)
    predictions = model.predict(test)

    output_test_data = pd.DataFrame() 
    output_test_data['Category'] = predictions.astype(int)

    output_test_data['Id'] = list(np.arange(1,predictions.size+1))

    submission = output_test_data[['Id','Category']]
    submission.to_csv(title, index=False)
    submission.head()
    return submission

##### Plsss change the title........
output = predict_and_submission(X_test,model,title = "Model_2.csv")


#######################################################################################################
#######################################################################################################
#######################################################################################################

## imports here !!!
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

from sklearn.impute import SimpleImputer

import random
random.seed(10)



'''
Importing data
'''
train_data= pd.read_csv('iith_foml_2020_train.csv')
train = pd.DataFrame(train_data)   ### Raw data
test_data= pd.read_csv('iith_foml_2020_test.csv')
test = pd.DataFrame(test_data)    ### Raw data
test.head()



#test.describe()



def imputing_missing_values(df):
    data = df.to_numpy()
    # define the imputer
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    imputer  = imputer.fit(data)
    # transform the dataset
    transformed_values = imputer.transform(data)
    imputed_data = pd.DataFrame(data = transformed_values,columns = df.columns) 
    return imputed_data


L1_train = imputing_missing_values(train)
L1_test = imputing_missing_values(test)



def normalize(df):
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


'''
Dividing into X, Y
'''


L2_train = L1_train.drop(columns=['Feature 16', 'Feature 17'],axis = 1)
L2_test = L1_test.drop(columns=['Feature 16', 'Feature 17'],axis = 1)

L3_train = L2_train   #### Add remove outliers here to do
L3_test = L2_test


#################################################################################

X = L3_train.drop(columns=['Target Variable (Discrete)'],axis = 1)
Y = L3_train[['Target Variable (Discrete)']]
X_test = L3_test




'''
Training with stratified K-fold with random forest
'''

i=1

splits = 10
kf = StratifiedKFold(n_splits= splits,random_state=1,shuffle=True)



accuracy = [0]* splits
for train_index,test_index in kf.split(X,Y):
    print('\n{} of kfold {}'.format(i,kf.n_splits))
    xtr,xvl = X.loc[train_index],X.loc[test_index]
    ytr,yvl = Y.loc[train_index],Y.loc[test_index]

    model = RandomForestClassifier(n_estimators=1000, bootstrap = True,max_features = 'sqrt')
    model.fit(xtr, ytr)

    #print (model.best_params_)
    y_pred=model.predict(xvl)
    y_pred = [round(value) for value in y_pred]
    
    
    print('accuracy_score',accuracy_score(yvl,y_pred) * 100)
    accuracy[i-1] = accuracy_score(yvl,y_pred) * 100
    i+=1

def predict_and_submission(test_data,model,title):### test_data in pd format
    test = pd.DataFrame(test_data)
    predictions = model.predict(test)

    output_test_data = pd.DataFrame() 
    output_test_data['Category'] = predictions.astype(int)

    output_test_data['Id'] = list(np.arange(1,predictions.size+1))

    submission = output_test_data[['Id','Category']]
    submission.to_csv(title, index=False)
    submission.head()
    return submission

##### Plsss change the title........
output = predict_and_submission(X_test,model,title = "Model_3.csv")



#######################################################################################################
#######################################################################################################
#######################################################################################################


###### Ensembling of all models..
## imports here !!!
import numpy as np
import pandas as pd
import xgboost as xgb


from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

import random
random.seed(10)


def generate_majoriy_vote(df_list,title):
    
    Majority_vote = pd.DataFrame()
    df = pd.DataFrame( pd.read_csv(df_list[0]) )
    Majority_vote['Id'] = df['Id']
    
    for i in range(len(df_list)):
        df = pd.DataFrame( pd.read_csv(df_list[i]) )
        Majority_vote[df_list[i]] = df['Category']
        
    Majority_vote["Ensemble"] = Majority_vote.mode(axis=1)[0].astype(int)
    

    ### Creating ensemble submission
    submission = pd.DataFrame() 
    
    submission['Id'] = Majority_vote ['Id']
    submission['Category'] = Majority_vote["Ensemble"]
    

    ### Creating csv
    #submission = output_test_data[['Id','Category']]
    submission.to_csv(title, index=False)    
        
    return Majority_vote

pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.max_rows', None)

df_list = ['Model_1.csv','Model_2.csv','Model_3.csv']
Majority = generate_majoriy_vote( df_list, "Ensemble.csv" )




