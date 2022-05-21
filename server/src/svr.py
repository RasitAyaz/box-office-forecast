
import pandas as pd
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statistics import mean
current_path = os.path.dirname(__file__)

dataset_path = f'{current_path}/../dataset.csv'

# Step 1 - Load Data

data = pd.read_csv(dataset_path)
X = data.iloc[: ,0:-1].values
y = data.iloc[:, -1].values

column_num_minus = len(data.columns) - 1
X = X.reshape(-1,column_num_minus)
y = y.reshape(-1,1)

X_train, X_test, y_train, y_test = train_test_split(X, y)

# Step 2 - Feature Scaling

sc_X = StandardScaler()
sc_y = StandardScaler()
X = sc_X.fit_transform(X)
y = sc_y.fit_transform(y)


# Step 3 - Fit SVR

from sklearn.svm import SVR
regressor = SVR(kernel = "linear")
regressor.fit(X_train,y_train.ravel())


def r2score(y_pred, y):
    rss = np.sum((y_pred - y) ** 2)
    tss = np.sum((y-y.mean()) ** 2)

    r2 = 1 - (rss / tss)
    return r2

def calculate_smape(y_test, y_pred):
    A = np.array(y_test)
    F = np.array(y_pred)
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))

# First transform 6.5 to feature scaling

sc_X_val = sc_X.transform(np.array([[6.5]*column_num_minus]))

# Second predict the value

scaled_y_pred = regressor.predict(X_test)
scaled_y_pred = scaled_y_pred.reshape(-1,1)

# Third - since this is scaled - we have to inverse transform

y_pred = sc_y.inverse_transform(scaled_y_pred)

# Compute r2 score and smape result

r2 = r2score(y_pred, y_test)
print(f'r^2: {r2}')
smape = calculate_smape(y_test, y_pred)
print(f'SMAPE (%): {smape}')





