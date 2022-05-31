from bisect import bisect
import os
import pickle
import bisect

from genericpath import isfile
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
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
        if x > a[mid]:
            hi = mid
        else:
            lo = mid+1
    a.insert(lo, x)


def calculate_smape(y_test, y_pred):
    A = np.array(y_test)
    F = np.array(y_pred)
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))


data = read_dataset()
data = standardize(data)

X = data.drop('revenue', axis=1)
y = data['revenue']

# Initialize array to measure linear regression.
lr_arr = []
mape_list = []
mse_list = []
for i in range(100):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    lr = LinearRegression().fit(X_train, y_train)

    # linear regression model r^2 score on test data
    score = lr.score(X_test, y_test)
    reverse_insort(lr_arr, score)

    # linear regression model mape on test data
    smape = calculate_smape(y_test, lr.predict(X_test))
    bisect.insort(mape_list, smape)

    # linear regression model rmse on test data
    mse = mean_squared_error(y_test, lr.predict(X_test))
    bisect.insort(mse_list, mse)


sum_score,  i, avg = 0, 0, 0

for x in lr_arr:
    if i <= 10:
        sum_score += x
    i += 1
avg = float(sum_score / 10)

print(f'Linear regression average score value is {avg}')

sum_mape, i, avg = 0, 0, 0
for x in mape_list:
    if i <= 10:
        sum_mape += x

    i += 1
avg = float(sum_mape / 10)

print(f'Linear regression average mape value is {avg}')

sum_mse, i, avg = 0, 0, 0
for x in mse_list:
    if i <= 10:
        sum_mse += x

    i += 1
avg = float(sum_mse / 10)

print(f'Linear regression average mse value is {avg}')

# Store linear regression the model to disk
filename = '{current_path}/../models/linear_regression.sav'.format(
    current_path=current_path)
pickle.dump(lr, open(filename, 'wb'))

print('---------------------------')

# Initialize array to measure artificial neural network regression.
ann_arr = []
rmse_ann_list = []
mse_ann_list = []
for i in range(100):
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    ann = MLPRegressor(max_iter=500, hidden_layer_sizes=10,
                       learning_rate_init=0.005).fit(X_train, y_train)

    # ANN model r^2 score on test data
    score = ann.score(X_test, y_test)
    reverse_insort(ann_arr, score)

    # ANN model smape on test data
    smape = calculate_smape(y_test, ann.predict(X_test))
    bisect.insort(rmse_ann_list, smape)

    # linear regression model rmse on test data
    mse = mean_squared_error(y_test, ann.predict(X_test))
    bisect.insort(mse_ann_list, mse)


sum_score,  i, avg = 0, 0, 0

for x in ann_arr:
    if i <= 10:
        sum_score += x
    i += 1
avg = float(sum_score / 10)

print(f'ANN average score value is {avg}')
sum_ann_mape, i, avg = 0, 0, 0
for x in rmse_ann_list:
    if i <= 10:
        sum_ann_mape += x

    i += 1
avg = float(sum_ann_mape / 10)

print(f'ANN average mape value is {avg}')

sum_mse, i, avg = 0, 0, 0
for x in mse_ann_list:
    if i <= 10:
        sum_mse += x

    i += 1
avg = float(sum_mse / 10)

print(f'ANN average mse value is {avg}')

# # Store artificial neural network the model to disk
# filename = '{current_path}/../models/artificial_neural_network.sav'.format(current_path=current_path)
# pickle.dump(ann, open(filename, 'wb'))
#
# print('---------------------------')
#
# # Initialize array to measure linear regression.
# svr_arr = []
# for i in range(100):
#     X_train, X_test, y_train, y_test = train_test_split(X, y)
#     svr = make_pipeline(SVR(kernel = "linear", C=1.0, epsilon=0.2)).fit(X_train, y_train)
#
#     # svr r^2 score for test data
#     score = svr.score(X_test, y_test)
#     reverse_insort(svr_arr, score)
#
# i = 0
# sum = 0
# avg = 0
#
# for x in svr_arr:
#     if i < 10:
#         sum += x
#         print(f'Value {i}:{x}')
#     i += 1
# avg = float(sum / 10)
#
# print(f'Support vector regression average score value is {avg}')
#
# # store support vector regression the model to disk
# filename = '{current_path}/../models/support_vector_regression.sav'.format(current_path=current_path)
# pickle.dump(svr, open(filename, 'wb'))
#
# print('---------------------------')
