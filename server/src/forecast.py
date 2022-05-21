import os

import pandas as pd
from genericpath import isfile

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
