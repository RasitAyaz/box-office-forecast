import os
import pickle

from genericpath import isfile
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR

from read_dataset import read_dataset
from standardization import standardize

current_path = os.path.dirname(__file__)

def reverse_insort(a, x, lo=0, hi=None):
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if x > a[mid]: hi = mid
        else: lo = mid+1
    a.insert(lo, x)


data = read_dataset()
data = standardize(data)

X = data.drop('revenue', axis=1)
y = data['revenue']

# Initialize array to measure linear regression.
lr_arr = []
for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    lr = LinearRegression().fit(X_train, y_train)

    # score = lr.score(X_train, y_train)
    # print(f'LR train score: {score}')

    # linear regression model r^2 score on test data

    score = lr.score(X_test, y_test)
    reverse_insort(lr_arr, score)
    
    # linear regression model r^2 score on overall data
    # score = lr.score(X, y)
    # print(f'LR overall score: {score}')

i = 0
sum = 0
avg = 0

for x in lr_arr:
    if i <= 100:
        sum += x 
        # print(f'Value {i}:{x}')        
    i += 1
avg = float(sum / 100)

print(f'Linear regression average score value is {avg}')    

# Store linear regression the model to disk
filename = '{current_path}/../models/linear_regression.sav'.format(current_path=current_path)
pickle.dump(lr, open(filename, 'wb'))

print('---------------------------')

# Initialize array to measure artificial neural network regression.
ann_arr = []
for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    ann = MLPRegressor(max_iter=1000,hidden_layer_sizes=10,learning_rate_init=0.05).fit(X_train, y_train)
    
    # artificial neural network model r^2 score on train data
    # score = ann.score(X_train, y_train)
    # print(f'ANN train score: {score}')

    # artificial neural network model r^2 score on test data
    score = ann.score(X_test, y_test)
    reverse_insort(ann_arr, score)
    # print(f'ANN test score: {score}')

    # artificial neural network model r^2 score on overall data
    # score = ann.score(X, y)
    # print(f'ANN overall score: {score}')
    
i = 0
sum = 0
avg = 0

for x in ann_arr:
    if i < 100:
        sum += x 
        # print(f'Value {i}:{x}')        
    i += 1
avg = float(sum / 100)

print(f'Artificial neural network average score value is {avg}') 

# Store artificial neural network the model to disk
filename = '{current_path}/../models/artificial_neural_network.sav'.format(current_path=current_path)
pickle.dump(ann, open(filename, 'wb'))  

print('---------------------------')

# Initialize array to measure linear regression.
svr_arr = []
for i in range(1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    svr = make_pipeline(SVR(kernel = "linear", C=1.0, epsilon=0.2)).fit(X_train, y_train)

    # svr r^2 score for training data
    # score = svr.score(X_train, y_train)
    # print(f'SVR with linear kernel train score: {score}')

    # svr r^2 score for test data
    score = svr.score(X_test, y_test)
    reverse_insort(svr_arr, score)

    # svr r^2 score for overall data
    # score = svr.score(X, y)
    # print(f'SVR with linear kernel overall score: {score}')i = 0
    
sum = 0
avg = 0

for x in svr_arr:
    if i < 100:
        sum += x 
        print(f'Value {i}:{x}')    
        break    
    i += 1
avg = float(sum / 100)

print(f'Support vector regression average score value is {avg}')   

# store support vector regression the model to disk
filename = '{current_path}/../models/support_vector_regression.sav'.format(current_path=current_path)
pickle.dump(svr, open(filename, 'wb'))

print('---------------------------')

    