import csv
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from genericpath import isfile
from scipy import stats
from sklearn import preprocessing

from movie_to_vector import movie_to_vector
from read_impacts import read_impacts

current_path = os.path.dirname(__file__)
data_path = f'{current_path}/../data'


def get_id(item):
    if 'iso_3166_1' in item:
        return item['iso_3166_1']
    if 'iso_639_1' in item:
        return item['iso_639_1']
    return item['id']


def get_name(item):
    if 'english_name' in item:
        return item['english_name']
    return item['name']


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


def get_impact(id, impact_data: pd.DataFrame):
    search_data = impact_data.loc[impact_data['id'] == id]
    if len(search_data) == 0:
        return None
    else:
        return search_data.iloc[0]['importance']


def get_list_impact(list, impact_data):
    impact_max = 0
    impact_sum = 0

    for item in list:
        impact = get_impact(get_id(item), impact_data)
        if impact is None:
            continue
        impact_sum += impact
        impact_max = max(impact_max, impact)

    if len(list) == 0 or impact_max == 0:
        return pd.NA, pd.NA
    else:
        impact_avg = impact_sum / len(list)
        return impact_avg, impact_max


def get_diminishing_list_impact(list, impact_data):
    order = 1
    impact_sum = 0
    weight_sum = 0

    for item in list:
        impact = get_impact(get_id(item), impact_data)
        if impact is None:
            continue
        weight = 1 / order
        impact = impact * weight
        order += 1
        impact_sum += impact
        weight_sum += weight

    if weight_sum == 0:
        return pd.NA
    else:
        return impact_sum


impacts = read_impacts()

data_items = []

for year in range(1990, 2020):
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


def standardize(data: pd.DataFrame):
    columns = data.columns
    scaler = preprocessing.StandardScaler()
    data = scaler.fit_transform(data)
    return pd.DataFrame(data, columns=columns)

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
data = standardize(data)

dataset_path = f'{current_path}/../dataset.csv'
data.to_csv(dataset_path, index=False)

