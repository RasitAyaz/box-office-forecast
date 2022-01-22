import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def read_dataset():
    return None


def find_cost(x: np.ndarray, y, w, b):
    cost = np.sum((((x.dot(w) + b) - y) ** 2) / (2 * len(y)))
    return cost


def apply_gradient_descent(x, y, weight, bias, learning_rate, epochs):
    cost_list = [0] * epochs

    for epoch in range(epochs):
        z = x.dot(weight) + bias
        loss = z - y

        weight_gradient = x.T.dot(loss) / len(y)
        bias_gradient = np.sum(loss) / len(y)

        weight = weight - learning_rate * weight_gradient
        bias = bias - learning_rate * bias_gradient

        cost = find_cost(x, y, weight, bias)
        cost_list[epoch] = cost

        if (epoch % (epochs / 10) == 0):
            print(f"Cost at epoch {epoch} is {cost}")

    return weight, bias, cost_list


def predict(x: np.ndarray, weight, bias):
    return x.dot(weight) + bias


def calculate_r2score(y_predicted, y):
    rss = np.sum((y_predicted - y) ** 2)
    tss = np.sum((y - y.mean()) ** 2)

    r2 = 1 - (rss / tss)
    return r2


def run(x, y):
    x_train: np.ndarray
    x_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=100
    )

    weight, bias, cost_list = apply_gradient_descent(
        x_train, y_train, np.zeros(x_train.shape[1]), 0, 0.001, epochs=15000
    )

    y_predicted = predict(x_test)

    print()
