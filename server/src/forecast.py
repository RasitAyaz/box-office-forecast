import os
import pickle

import pandas as pd
from genericpath import isfile
from numpy import ndarray
from sklearn.linear_model import LinearRegression

from format_movie_json import format_movie_json
from movie_to_vector import movie_to_vector
from read_impacts import read_impacts

current_path = os.path.dirname(__file__)


def forecast_with_linear_regression(movie):
    movie = format_movie_json(movie)
    model_path = f'{current_path}/models/linear_regression.csv'
    model_data = pd.read_csv(model_path)
    vector: dict
    vector = movie_to_vector(movie, read_impacts())

    sum = 0
    for feature, value in vector.items():
        sum += value * model_data.iloc[0][feature]

    return sum / len(vector)

def forecast_linear_regression(X):
    filename = f'{current_path}/../models/linear_regression.sav'
    model: LinearRegression
    model = pickle.load(open(filename, 'rb'))
    y: ndarray
    y = model.predict(X)
    return y.flat[-1]

def forecast_artificial_neural_network(movie):
    filename = '{current_path}/../models/artificial_neural_network.sav'.format(current_path=current_path)
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model.predict()

def forecast_support_vector_regression(movie):
    filename = '{current_path}/../models/support_vector_regression.sav'.format(current_path=current_path)
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model.predict()
    
