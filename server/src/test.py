from audioop import cross
from genericpath import isfile
import os
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import cross_val_score, train_test_split


current_path = os.path.dirname(__file__)
dataset_path = f'{current_path}/../dataset.csv'

if isfile(dataset_path):
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')
    
df = data.copy()
X = df.drop("revenue", axis=1)
y = df["revenue"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state= 100)

lm = LinearRegression()
model = lm.fit(X_train, y_train)


rmse = np.sqrt(mean_squared_error(y_train, model.predict(X_train)))
print(f'rmse(train): {rmse}')

rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
print(f'rmse(test): {rmse}')

score = model.score(X_train,y_train)
print(f'score: {score}')

cross_val_score = cross_val_score(model,X,y,cv=10,scoring ="r2").mean()
print(f'cross val mean score: {cross_val_score}')

mape = mean_absolute_percentage_error(y_test, model.predict(X_test))
print(f'mape: {mape}')


    