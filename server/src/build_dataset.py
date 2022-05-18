import csv
import json
import os
from datetime import datetime

import numpy as np
import pandas as pd
from genericpath import isfile
from scipy import stats
from sklearn import preprocessing

current_path = os.path.dirname(__file__)


def read_json_file(path):
    if isfile(path):
        return json.load(open(path))
    else:
        print(f'{path} could not be found.')
        exit()


directors_json = read_json_file(f'{current_path}/../data/directors.json')
stars_json = read_json_file(f'{current_path}/../data/stars.json')
companies_json = read_json_file(f'{current_path}/../data/companies.json')
genres_json = read_json_file(f'{current_path}/../data/genres.json')


def get_year(date):
    return int(date[0:4])


def calculate_growing_impact(list, json, date):
    impact_max = 0
    impact_sum = 0

    for item in list:
        json_item = json[str(item['id'])]
        value_sum = 0
        factor_sum = 0
        for credit in json_item['credits']:
            if credit['date'] >= date:
                break
            year_diff = get_year(date) - get_year(credit['date'])
            factor = 1 / (year_diff + 1)
            value_sum += credit['value'] * factor
            factor_sum += factor

        if factor_sum == 0:
            continue

        impact = value_sum / factor_sum
        impact_sum += impact
        impact_max = max(impact_max, impact)

    impact_avg = impact_sum / len(list)
    return impact_avg, impact_max


def calculate_genre_impact(genres):
    impact_sum = 0
    n_genres = 0

    for genre in genres:
        id = str(genre['id'])
        if id in genres_json:
            impact_sum += genres_json[id]['value']
            n_genres += 1

    return impact_sum / n_genres


headers = [
    'budget',
    'director_max',
    'star_avg',
    'star_max',
    'company_avg',
    'company_max',
    'company_count',
    # 'genre_impact',
    'producer_count',
    'runtime',
    'revenue',
]


dataset_path = f'{current_path}/../dataset.csv'

with open(dataset_path, 'w', newline='') as dataset:
    writer = csv.writer(dataset)
    writer.writerow(headers)
    for year in range(1990, 2020):
        movies: dict
        movies = read_json_file(f'{current_path}/../data/years/{year}.json')
        for id, movie in movies.items():
            date = movie['release_date']
            directors = [p for p in movie['crew']
                         if p['job'] == 'Director']
            stars = movie['cast'][:3]
            if len(stars) == 0:
                continue

            companies = movie['production_companies']
            if len(companies) == 0:
                continue

            genres = movie['genres']
            producer_count = 0

            for person in movie['crew']:
                if person['department'] == 'Production':
                    producer_count += 1

            if producer_count == 0:
                continue

            director_avg, director_max = calculate_growing_impact(
                directors, directors_json, date)
            star_avg, star_max = calculate_growing_impact(
                stars, stars_json, date)
            company_avg, company_max = calculate_growing_impact(
                companies, companies_json, date)

            if director_max == 0 or star_max == 0 or company_max == 0:
                continue

            if len(companies) > 0 and len(genres) > 0:
                writer.writerow([
                    movie['budget'],
                    director_max,
                    star_avg,
                    star_max,
                    company_avg,
                    company_max,
                    len(companies),
                    # calculate_genre_impact(genres),
                    producer_count,
                    movie['runtime'],
                    movie['revenue'],
                ])


def remove_all_outliers(data):
    return data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]


def remove_outliers(data):
    cols = [
        'budget'
    ]

    for col in cols:
        data = data[(np.abs(stats.zscore(data[col])) < 3)]

    return data


data = pd.read_csv(dataset_path)
print(f'Data size: {len(data)}')
# Removes all outliers
# data = remove_all_outliers(data)
print(f'Data size after outlier removal: {len(data)}')
# data = pd.DataFrame(preprocessing.scale(data.astype(float)), columns=headers)
data.to_csv(dataset_path, index=False)
