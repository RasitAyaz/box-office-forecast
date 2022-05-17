import csv
import json
import os
from datetime import datetime

import pandas as pd
from genericpath import isfile
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


def calculate_growing_impact(list, json, date):
    impact_sum = 0

    for item in list:
        json_item = json[str(item['id'])]
        value_sum = 0
        n_credits = 0
        for credit in json_item['credits']:
            if credit['date'] > date:
                break
            value_sum += credit['value']
            n_credits += 1

        impact_sum += value_sum / n_credits

    return impact_sum / len(list)


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
    'director_impact',
    'star_impact',
    'company_impact',
    # 'genre_impact',
    'producer_count',
    'revenue',
]


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
            stars = movie['cast'][:5]
            if len(stars) == 0:
                continue
            companies = movie['production_companies']
            genres = movie['genres']
            producer_count = 0

            for person in movie['crew']:
                if person['department'] == 'Production':
                    producer_count += 1

            if len(companies) > 0 and len(genres) > 0:
                writer.writerow([
                    movie['budget'],
                    calculate_growing_impact(directors, directors_json, date),
                    calculate_growing_impact(stars, stars_json, date),
                    calculate_growing_impact(companies, companies_json, date),
                    # calculate_genre_impact(genres),
                    producer_count,
                    movie['revenue'],
                ])

data = pd.read_csv(dataset_path)
data = remove_outliers(data)
data = pd.DataFrame(preprocessing.scale(data), columns=headers)
data.to_csv(dataset_path, index=False)
