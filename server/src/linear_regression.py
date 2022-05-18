import json
import os
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from genericpath import isfile
from importlib_metadata import csv
from sklearn.metrics import (mean_absolute_error,
                             mean_absolute_percentage_error,
                             mean_squared_error)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

current_path = os.path.dirname(__file__)


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

        # if epoch % 100 == 0:
        #     print(f'Epoch {epoch} / {epochs}')
        #     print(bias)
        #     print()

    return weights, bias, costs


def calculate_mape(y, y_pred):
    return np.sum(abs((y - y_pred) / y)) / len(y)


def r2score(y_pred, y):
    rss = np.sum((y_pred - y) ** 2)
    tss = np.sum((y-y.mean()) ** 2)

    r2 = 1 - (rss / tss)
    return r2


def predict(X: np.ndarray, weights, bias):
    return X.dot(weights) + bias


def calculate_smape(y_test, y_pred):
    A = np.array(y_test)
    F = np.array(y_pred)
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))


def build_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=100
    )

    epochs = 1000
    print(f'number of epochs: {epochs}')

    weights, bias, costs = gradient_descent_function(
        X_train, y_train,
        weights=np.random.randn(X_train.shape[1]),
        bias=0,
        learning_rate=0.05,
        epochs=epochs,
    )

    y_pred = predict(X_test, weights, bias)
    r2 = r2score(y_pred, y_test)
    print(f'r^2: {r2}')
    smape = calculate_smape(y_test, y_pred)
    print(f'SMAPE (%): {smape}')

    # plt.plot(costs)
    # plt.xlabel('epochs')
    # plt.ylabel('cost')
    # plt.show()

    return {
        'bias': bias,
        'weights': weights.tolist(),
    }

    some_data = [[20000000, 21637263.0,
                  68001989.73611112, 32916185.11897275, 41637263]]
    df = pd.DataFrame(some_data, columns=[
                      'budget', 'director_impact', 'star_impact', 'company_impact', 'revenue'])

    X2 = df.iloc[:, 0:-1]
    y2 = df.iloc[:, -1]

    sc = StandardScaler()
    X2 = sc.fit_transform(X2)

    print(f'{y2[0]}: {predict(X2, weights, bias)}')

    # plt.scatter(X[:, 0], y, color=(1, 0, 0, 0.25), edgecolors='none')
    # plt.plot(X_test, y_pred, color='blue')
    # plt.show()


def store_model(model, headers: list):
    # Remove revenue header
    headers.pop()
    # Add bias header
    headers.insert(0, 'bias')

    values: list = model['weights']
    values.insert(0, model['bias'])

    with open(f'{current_path}/../models/linear_regression.csv', 'w', newline='') as model_file:
        writer = csv.writer(model_file)
        writer.writerow(headers)
        writer.writerow(values)


dataset_path = f'{current_path}/../dataset.csv'

if isfile(dataset_path):
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')

    X = data.iloc[:, 0:-1]
    y = data.iloc[:, -1]

    sc = StandardScaler()
    X = sc.fit_transform(X)

    model = build_model(X, y)

    store_model(model, list(data))


else:
    print(f'{dataset_path} could not be found.')
