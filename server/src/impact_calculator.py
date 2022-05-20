import json
import operator
import os

import pandas as pd
from genericpath import isfile
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from xgboost import XGBRegressor

current_path = os.path.dirname(__file__)


def calculate_correlation(data):
    x = data['star_avg']
    y = data['revenue']
    x.corr(y, method='spearman')
    test_stats, p_value = pearsonr(x, y)
    print(f'{test_stats}, {p_value}')


def count_features(counts, feature_items):
    for item in feature_items:
        id = item['id']
        name = item['name']
        if id not in counts:
            counts[id] = {'name': name, 'count': 1}
        else:
            counts[id]['count'] += 1


def set_min_count(counts: dict, min_count):
    for id in list(counts.keys()):
        if counts[id]['count'] < min_count:
            del counts[id]


def sort_counts(counts: dict):
    return {k: v for k, v in sorted(counts.items(), key=lambda item: item[1]['count'], reverse=True)}


def prepare_feature(feature, counts, min_count, print_list: bool):
    total = len(counts)
    set_min_count(counts, min_count)
    counts = sort_counts(counts)
    print('--------------------------------')
    print(f'Total {feature}: {len(counts)} / {total} (>= {min_count})')
    if print_list:
        print('--------------------------------')
        for id, genre in counts.items():
            print(f'{genre["name"]}: {genre["count"]}')


def add_feature_columns(row, movie_items, counts: dict):
    for id, item in counts.items():
        row[f'{id}'] = 0

    for item in movie_items:
        id = item['id']
        if id in counts:
            row[f'{id}'] = 1


genre_counts = {}
company_counts = {}
star_counts = {}

all_movies = []

for year in range(1990, 2020):
    path = f'{current_path}/../data/years/{year}.json'
    if isfile(path):
        movies_of_year = json.load(open(path))
        for id, movie in movies_of_year.items():
            # Skip invalid movies
            if len(movie['genres']) == 0:
                continue
            
            all_movies.append(movie)
            count_features(genre_counts, movie['genres'])
            count_features(company_counts, movie['production_companies'])
            count_features(star_counts, movie['cast'])
    else:
        print(f'{path} could not be found.')
        exit()

print('--------------------------------')
print(f'Total movies: {len(all_movies)}')


def display_impacts(feature, sorted_importances):
    xs, ys = [*zip(*sorted_importances)]
    plt.rcdefaults()
    fig, ax = plt.subplots()
    plt.barh(xs, ys)
    ax.invert_yaxis()
    ax.set_title(feature)
    plt.xlabel('Feature importance score')
    plt.show()


def calculate_impacts(feature, movie_feature, counts):
    data_items = []

    for movie in all_movies:
        row = {}
        add_feature_columns(row, movie[movie_feature], counts)
        row['revenue'] = movie['revenue']
        data_items.append(row)

    data: pd.DataFrame
    data = pd.DataFrame(data_items)
    X = data.iloc[:, 0:-1]
    X_headers = data.columns[0:-1].values
    y = data.iloc[:, -1]

    regressor = XGBRegressor()
    regressor.fit(X, y)

    importances = {}

    count = 0
    for feature_importance in regressor.feature_importances_:
        if feature_importance > 0.002:
            feature_id = X_headers[count]
            importances[feature_id] = feature_importance
        count += 1

    importances = {k: v for k, v in sorted(importances.items(), key=lambda item: item[1], reverse=True)}
    # Get top 40 features
    # sorted_importances = sorted_importances[0:40]

    # display_impacts(feature, sorted_importances)

    return importances

def store_impacts_to_csv(feature, importances):
    data = pd.DataFrame(importances.items(), columns=['id', 'importance'])
    path = f'{current_path}/../data/impacts/{feature}.csv'
    data.to_csv(path, index=False)


prepare_feature('genres', genre_counts, min_count=15, print_list=False)
prepare_feature('companies', company_counts, min_count=15, print_list=False)
prepare_feature('stars', star_counts, min_count=15, print_list=False)


importances = calculate_impacts('genres', 'genres', genre_counts)
store_impacts_to_csv('genres', importances)

importances = calculate_impacts('companies', 'production_companies', company_counts)
store_impacts_to_csv('companies', importances)

importances = calculate_impacts('stars', 'cast', star_counts)
store_impacts_to_csv('stars', importances)

