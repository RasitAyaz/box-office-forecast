import os

import pandas as pd
from genericpath import isfile
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVR

current_path = os.path.dirname(__file__)
dataset_path = f'{current_path}/../dataset.csv'

if isfile(dataset_path):
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')
    
df = data.copy()
X = df.drop("revenue", axis=1)
y = df["revenue"]

print('---------------------------')

X_train, X_test, y_train, y_test = train_test_split(X, y)
lr = LinearRegression().fit(X_test, y_test)

score = lr.score(X_train, y_train)
print(f'LR train score: {score}')

score = lr.score(X_test, y_test)
print(f'LR test score: {score}')

score = lr.score(X, y)
print(f'LR overall score: {score}')

print('---------------------------')

X_train, X_test, y_train, y_test = train_test_split(X, y)
ann = MLPRegressor(max_iter=1000,hidden_layer_sizes=2,learning_rate_init=0.05).fit(X_train, y_train)

score = ann.score(X_train, y_train)
print(f'ANN train score: {score}')

score = ann.score(X_test, y_test)
print(f'ANN test score: {score}')

score = ann.score(X, y)
print(f'ANN overall score: {score}')

print('---------------------------')

X_train, X_test, y_train, y_test = train_test_split(X, y)
svr = make_pipeline(SVR(C=1.0, epsilon=0.2)).fit(X_train, y_train)

score = svr.score(X_train, y_train)
print(f'SVR train score: {score}')

score = svr.score(X_test, y_test)
print(f'SVR test score: {score}')

score = svr.score(X, y)
print(f'SVR overall score: {score}')

    