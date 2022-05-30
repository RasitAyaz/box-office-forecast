import json
import os

import numpy as np
import pandas as pd
from genericpath import isfile
from scipy import stats

from movie_to_vector import movie_to_vector
from read_impacts import read_impacts

current_path = os.path.dirname(__file__)
data_path = f'{current_path}/../data'


def read_json_file(path):
    if isfile(path):
        return json.load(open(path))
    else:
        print(f'{path} could not be found.')
        exit()


def get_year(date):
    return int(date[0:4])


def get_month(date):
    return int(date[5:7])


impacts = read_impacts()

data_items = []

for year in range(1991, 2020):
    print(f'Processing year {year}...', end='\r')
    movies: dict
    movies = read_json_file(f'{current_path}/../data/years/{year}.json')
    for id, movie in movies.items():
        vector = movie_to_vector(movie, impacts)
        if vector is not None:
            data_items.append(vector)


def remove_all_outliers(data):
    return data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]


def remove_outliers(data):
    cols = [
        'budget'
    ]

    for col in cols:
        data = data[(np.abs(stats.zscore(data[col])) < 3)]

    return data

data: pd.DataFrame
data = pd.DataFrame(data_items)

# Fill empty features with average value
data = data.fillna(data.mean())

print(end='\x1b[2K')
print(f'Data size: {len(data)}')

# Removes all outliers
# data = remove_all_outliers(data)
# print(f'Data size after outlier removal: {len(data)}')

# Standardization
# data = standardize(data)

dataset_path = f'{current_path}/../dataset.csv'
data.to_csv(dataset_path, index=False)

