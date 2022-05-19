import os

import pandas as pd
from genericpath import isfile
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor

current_path = os.path.dirname(__file__)
dataset_path = f'{current_path}/../dataset.csv'

if isfile(dataset_path):
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')
    
df = data.copy()
X = df.drop("revenue", axis=1)
y = df["revenue"]

print('---------------------------')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state= 100)

lr = LinearRegression().fit(X_test, y_test)

score = lr.score(X_train, y_train)
print(f'LR train score: {score}')

score = lr.score(X_test, y_test)
print(f'LR test score: {score}')

score = lr.score(X, y)
print(f'LR overall score: {score}')

print('---------------------------')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state= 100)

ann = MLPRegressor(max_iter=1000).fit(X_train, y_train)

score = ann.score(X_train, y_train)
print(f'ANN train score: {score}')

score = ann.score(X_test, y_test)
print(f'ANN test score: {score}')

score = ann.score(X, y)
print(f'ANN overall score: {score}')



    