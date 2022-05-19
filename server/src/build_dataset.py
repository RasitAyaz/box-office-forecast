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
data_path = f'{current_path}/../data'


def read_json_file(path):
    if isfile(path):
        return json.load(open(path))
    else:
        print(f'{path} could not be found.')
        exit()


directors_json = read_json_file(f'{data_path}/directors.json')
stars_json = read_json_file(f'{data_path}/stars.json')
companies_json = read_json_file(f'{data_path}/companies.json')
genres_json = read_json_file(f'{data_path}/genres.json')
months_json = read_json_file(f'{data_path}/months.json')
keywords_json = read_json_file(f'{data_path}/keywords.json')
languages_json = read_json_file(f'{data_path}/languages.json')
countries_json = read_json_file(f'{data_path}/countries.json')


def get_year(date):
    return int(date[0:4])


def get_month(date):
    return int(date[5:7])


def calculate_impact(id, json, date):
    json_item = json[str(id)]
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
        return 0
    else:
        return value_sum / factor_sum


def calculate_list_impact(list, json, date):
    impact_max = 0
    impact_sum = 0

    for item in list:
        if 'iso_3166_1' in item:
            id = item['iso_3166_1']
        elif 'iso_639_1' in item:
            id = item['iso_639_1']
        else:
            id = item['id']

        impact = calculate_impact(id, json, date)
        impact_sum += impact
        impact_max = max(impact_max, impact)


    if len(list) == 0 or impact_max == 0:
        return pd.NA, pd.NA
    else:
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
    'producer_count',
    'runtime',
    'month',
    'month_impact',
    'keyword_avg',
    'keyword_max',
    'language_avg',
    'language_max',
    'country_avg',
    'country_max',
    'revenue',
]

data_items = []

for year in range(2000, 2020):
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

        director_avg, director_max = calculate_list_impact(directors, directors_json, date)
        star_avg, star_max = calculate_list_impact(stars, stars_json, date)
        company_avg, company_max = calculate_list_impact(companies, companies_json, date)
        keyword_avg, keyword_max = calculate_list_impact(movie['keywords'], keywords_json, date)
        language_avg, language_max = calculate_list_impact(movie['spoken_languages'], languages_json, date)
        country_avg, country_max = calculate_list_impact(movie['production_countries'], countries_json, date)


        if len(companies) > 0 and len(genres) > 0:
            data_items.append({
                'budget': movie['budget'],
                'director_max': director_max,
                'star_avg': star_avg,
                'star_max': star_max,
                'company_avg': company_avg,
                'company_max': company_max,
                'company_count': len(companies),
                'producer_count': producer_count,
                'runtime': movie['runtime'],
                'month': get_month(date),
                'month_impact': calculate_impact(get_month(date), months_json, date),
                'keyword_avg': keyword_avg,
                'keyword_max': keyword_max,
                'language_avg': language_avg,
                'language_max': language_max,
                'country_avg': country_avg,
                'country_max': country_max,
                'revenue': movie['revenue'],
            })


def remove_all_outliers(data):
    return data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]


def remove_outliers(data):
    cols = [
        'budget'
    ]

    for col in cols:
        data = data[(np.abs(stats.zscore(data[col])) < 3)]

    return data


def standardize(data):
    scaler = preprocessing.StandardScaler()
    data = scaler.fit_transform(data)
    return pd.DataFrame(data, columns=headers)

data: pd.DataFrame
data = pd.DataFrame(data_items, columns=headers)

# Fill empty features with average value
data = data.fillna(data.mean())

print(f'Data size: {len(data)}')

# Removes all outliers
# data = remove_all_outliers(data)
# print(f'Data size after outlier removal: {len(data)}')

# Standardization
data = standardize(data)

dataset_path = f'{current_path}/../dataset.csv'
data.to_csv(dataset_path, index=False)
