from genericpath import isfile
import json
from statistics import mean
from importlib_metadata import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error
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


def build_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=100
    )

    weights, bias, costs = gradient_descent_function(
        X_train, y_train,
        weights=np.random.randn(X_train.shape[1]),
        bias=0,
        learning_rate=0.005,
        epochs=1000,
    )

    y_pred = predict(X_test, weights, bias)
    r2 = r2score(y_pred, y_test)
    print(f'r^2: {r2}')
    mae = mean_absolute_error(y_test, y_pred) * 100 / mean(y_test)
    print(f'MAE (%): {mae}')
    mse = mean_squared_error(
        y_test, y_pred, squared=True) * 100 / mean(y_test) ** 2
    print(f'MSE (%): {mse}')

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


def remove_outliers(data):
    cols = [
        'budget',
        # 'director_impact',
        # 'star_impact',
        # 'company_impact',
        # 'genre_impact',
        # 'revenue',
    ]

    Q1 = data[cols].quantile(0.25)
    Q3 = data[cols].quantile(0.75)
    IQR = Q3 - Q1
    data = data[~((data[cols] < (Q1 - 1.5 * IQR)) |
                  (data[cols] > (Q3 + 1.5 * IQR))).any(axis=1)]

    print(f'Data size after outlier removal: {len(data)}')

    return data


def store_model(model, headers: list):
    # Remove revenue header
    headers.pop()
    # Add bias header
    headers.insert(0, 'bias')

    values: list = model['weights']
    values.insert(0, model['bias'])

    with open('models/linear_regression.csv', 'w', newline='') as model_file:
        writer = csv.writer(model_file)
        writer.writerow(headers)
        writer.writerow(values)


dataset_path = 'data/dataset.csv'

if isfile(dataset_path):
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')

    data = remove_outliers(data)

    X = data.iloc[:, 0:-1]
    y = data.iloc[:, -1]

    sc = StandardScaler()
    X = sc.fit_transform(X)

    model = build_model(X, y)
    
    store_model(model, list(data))


else:
    print(f'{dataset_path} could not be found.')
