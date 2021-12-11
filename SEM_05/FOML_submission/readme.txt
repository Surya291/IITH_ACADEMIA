Modules used..

Please see that you have these versions installed..

Numpy version 1.18.1
pandas version 1.0.3
xg boost 0.90
sklearn 0.22.1  ***** Important

#################################################

Performance..

Public set :  0.93427
Private set : 0.94366

################################################### 

Summary.
==========

1. My model is an ensemble of three models.
2. I took 3 different models. 
	a) Xgboost  						----> Model1.csv
	b) Xgboost with different parameter			----> Model2.csv
	c) Random forest 					----> Model3.csv
3. At the end I took the majority vote of all of the 3 csv filess...
	The ensembled output is saved as 			----->"test_output.csv"
#########################################################

Conventions..

train input file  ----> train_input.csv
test  input file  ----> test_input.csv

test  output file -----> test_output.csv

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Instructions...
-------------


run ee18btech11026.py file.. 
Make sure you have the mentioned versions of models.



Expected output:

Output Model_1.csv  ,  Model_2.csv,  Model_3.csv  ::: induvidual model output

Actual output : test_output.csv ::: To be considered
#######################################################

P.S : 
I actually coded the three models in 3 different files, but for submitting as a single file. I 
cascaded all the 3 files. Please bare with the same modules being imported multiple times.
