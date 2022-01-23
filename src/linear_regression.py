from genericpath import isfile
from importlib_metadata import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def read_dataset():
    return None


def cost_function(X, y, weights, bias):
    return np.sum((((X.dot(weights) + bias) - y) ** 2) / (2 * len(y)))


def gradient_descent_function(X: np.ndarray, y, weights, bias, learning_rate, epochs):
    m = len(y)
    costs = [0] * epochs

    for epoch in range(epochs):
        # Forward Propagation
        z = X.dot(weights) + bias

        loss = z - y

        weight_gradient = X.T.dot(loss) / m
        bias_gradient = np.sum(loss) / m

        weights = weights - learning_rate * weight_gradient
        bias = bias - learning_rate * bias_gradient

        cost = cost_function(X, y, weights, bias)
        costs[epoch] = cost

    return weights, bias, costs


def r2score(y_pred, y):
    rss = np.sum((y_pred - y) ** 2)
    tss = np.sum((y-y.mean()) ** 2)

    r2 = 1 - (rss / tss)
    return r2


def predict(X: np.ndarray, weights, bias):
    return X.dot(weights) + bias


def run(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=100
    )

    weights, bias, costs = gradient_descent_function(
        X_train, y_train,
        weights=np.random.randn(X_train.shape[1]),
        bias=0,
        learning_rate=0.005,
        epochs=5000,
    )

    y_pred = predict(X_test, weights, bias)
    r2 = r2score(y_pred, y_test)
    print(f'r2: {r2}')
    error = mean_absolute_percentage_error(y_test, y_pred)
    print(f'MAPE: {error}')

    # plt.scatter(X[:, 0], y, color=(1, 0, 0, 0.25), edgecolors='none')
    # plt.plot(X_test, y_pred, color='blue')
    # plt.show()


def remove_outliers(data):
    cols = [
        # 'budget',
        # 'director_impact',
        # 'star_impact',
        'company_impact',
        'revenue',
    ]

    Q1 = data[cols].quantile(0.25)
    Q3 = data[cols].quantile(0.75)
    IQR = Q3 - Q1
    data = data[~((data[cols] < (Q1 - 1.5 * IQR)) |
                  (data[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

    print(f'Data size after outlier removal: {len(data)}')

    return data


dataset_path = 'data/dataset.csv'

if isfile(dataset_path):
    print('Reading dataset...')
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')

    data = remove_outliers(data)

    X = data.iloc[:, 0:-1]
    y = data.iloc[:, -1]

    sc = StandardScaler()
    X = sc.fit_transform(X)

    run(X, y)
else:
    print(f'{dataset_path} could not be found.')
