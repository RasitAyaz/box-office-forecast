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


def get_name(item):
    return item['name']


def calculate_impacts(movie_feature, counts: dict, min_importance):
    data_items = []

    for movie in all_movies:
        row = {}

        for id, item in counts.items():
            row[f'{id}'] = 0

        for item in movie[movie_feature]:
            id = item['id']
            if id in counts:
                row[f'{id}'] = 1
        
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
        if feature_importance > min_importance:
            feature_id = X_headers[count]
            importances[feature_id] = feature_importance
        count += 1

    # importances = {k: v for k, v in sorted(importances.items(), key=lambda item: item[1], reverse=True)}

    importance_data_items = []
    
    for id, item in counts.items():
        id = str(id)
        if id not in importances:
            continue
        
        importance_data_items.append({
            'id': id,
            'name': get_name(item),
            'importance': importances[id]
        })

    importance_data_items = sorted(importance_data_items, key=lambda item: item['importance'], reverse=True)

    importance_data: pd.DataFrame
    importance_data = pd.DataFrame(importance_data_items)

    # Get top 40 features
    # sorted_importances = sorted_importances[0:40]

    # display_impacts(feature, sorted_importances)

    return importance_data

def store_impacts_to_csv(feature, importance_data):
    data = pd.DataFrame(importance_data)
    path = f'{current_path}/../data/impacts/{feature}.csv'
    data.to_csv(path, index=False)


prepare_feature('genres', genre_counts, min_count=2, print_list=False)
prepare_feature('companies', company_counts, min_count=15, print_list=False)
prepare_feature('stars', star_counts, min_count=5, print_list=False)


importance_data = calculate_impacts('genres', genre_counts, min_importance=0.001)
store_impacts_to_csv('genres', importance_data)

importance_data = calculate_impacts('production_companies', company_counts, min_importance=0.001)
store_impacts_to_csv('companies', importance_data)

importance_data = calculate_impacts('cast', star_counts, min_importance=0.001)
store_impacts_to_csv('stars', importance_data)

