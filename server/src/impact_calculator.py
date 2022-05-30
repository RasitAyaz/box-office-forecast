import json
import os

import pandas as pd
from genericpath import isfile
from matplotlib import pyplot as plt
from xgboost import XGBRegressor

current_path = os.path.dirname(__file__)


def get_id(item):
    if 'iso_3166_1' in item:
        return item['iso_3166_1']
    if 'iso_639_1' in item:
        return item['iso_639_1']
    return str(item['id'])


def get_name(item):
    if 'english_name' in item:
        return item['english_name']
    return item['name']


def count_crew_members(crew):
    for person in crew:
        id = get_id(person)
        
        department = person['department']
        if department == 'Directing':
            counts = directing_counts
        elif department == 'Writing':
            counts = writing_counts
        elif department == 'Production':
            counts = production_counts
        elif department == 'Art':
            counts = art_counts
        elif department == 'Sound':
            counts = sound_counts
        elif department == 'Camera':
            counts = camera_counts
        elif department == 'Editing':
            counts = editing_counts
        elif department == 'Costume & Make-Up':
            counts = costume_counts
        else:
            continue

        if id not in counts:
            counts[id] = {'name': get_name(person), 'count': 1}
        else:
            counts[id]['count'] += 1


def get_month_name(month):
    if month == 1:
        return 'January'
    elif month == 2:
        return 'February'
    elif month == 3:
        return 'March'
    elif month == 4:
        return 'April'
    elif month == 5:
        return 'May'
    elif month == 6:
        return 'June'
    elif month == 7:
        return 'July'
    elif month == 8:
        return 'August'
    elif month == 9:
        return 'September'
    elif month == 10:
        return 'October'
    elif month == 11:
        return 'November'
    elif month == 12:
        return 'December'


def get_month(date):
    return int(date[5:7])


def count_month(month):
    if month not in month_counts:
        month_counts[month] = {'name': get_month_name(month), 'count': 1}
    else:
        month_counts[month]['count'] += 1


def count_original_language(language):
    if language not in original_language_counts:
        original_language_counts[language] = {'name': language, 'count': 1}
    else:
        original_language_counts[language]['count'] += 1


def count_features(counts, feature_items):
    for item in feature_items:
        id = get_id(item)
        if id not in counts:
            counts[id] = {'name': get_name(item), 'count': 1}
        else:
            counts[id]['count'] += 1


def set_min_count(counts: dict, min_count):
    for id in list(counts.keys()):
        if counts[id]['count'] < min_count:
            del counts[id]


def sort_counts(counts: dict):
    return {k: v for k, v in sorted(counts.items(), key=lambda item: item[1]['count'], reverse=True)}


def filter_by_count(feature, counts, min_count, print_list = False):
    total = len(counts)
    set_min_count(counts, min_count)
    counts = sort_counts(counts)
    print(f'{feature}: {len(counts)} / {total} (count >= {min_count})')
    print('----------------------------------------------------')
    if print_list:
        for id, genre in counts.items():
            print(f'{genre["name"]}: {genre["count"]}')
        print('----------------------------------------------------')


def display_impacts(feature, sorted_importances):
    xs, ys = [*zip(*sorted_importances)]
    plt.rcdefaults()
    fig, ax = plt.subplots()
    plt.barh(xs, ys)
    ax.invert_yaxis()
    ax.set_title(feature)
    plt.xlabel('Feature importance score')
    plt.show()


def store_impacts_to_csv(feature, impacts: dict):
    data_items = []
    for id, item in impacts.items():
        data_item = {
            'id': id,
            'name': item['name'],
        }

        for year in range(1990, 1995):
            if year not in item['impacts']:
                data_item[f'{year}'] = 0
            else:
                data_item[f'{year}'] = item['impacts'][year]
        
        data_items.append(data_item)

    data = pd.DataFrame(data_items)
    path = f'{current_path}/../data/impacts/{feature}.csv'
    data.to_csv(path, index=False)



def calculate_importances(year, feature, list_feature, counts: dict, lower_bound=0):
    data_items = []

    for movie in all_movies:
        row = {}

        if feature == 'months':
            for month_number, month in month_counts.items():
                row[month_number] = 0
            
            row[get_month(movie['release_date'])] = 1

        elif feature == 'original_languages':
            for code, language in original_language_counts.items():
                row[code] = 0
            
            if movie['original_language'] in original_language_counts:
                row[movie['original_language']] = 1

        else:
            for id, item in counts.items():
                row[id] = 0

            order = 1
            for item in movie[list_feature]:
                id = get_id(item)
                if id in counts:
                    row[id] = 1 / order
                order += 1
        
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
        if feature_importance > lower_bound:
            feature_id = X_headers[count]
            importances[feature_id] = feature_importance
        count += 1

    
    for id, item in counts.items():
        if id not in importances:
            continue

        if feature not in impact_json:
            impact_json[feature] = {}
        if id not in impact_json[feature]:
            impact_json[feature][id] = {
                'name': item['name'],
                'impacts': {year: importances[id]}
            }
        else:
            item_json = impact_json[feature][id]
            item_json['impacts'][year] = importances[id]
    
    print(f'{year} {feature}: {len(importances)} / {len(counts)} (importance > {lower_bound})')
    print('----------------------------------------------------')

impact_json = {}


for max_year in range(1991, 1995):
    month_counts = {}
    original_language_counts = {}

    genre_counts = {}
    company_counts = {}
    country_counts = {}
    language_counts = {}
    cast_counts = {}
    keyword_counts = {}

    directing_counts = {}
    writing_counts = {}
    production_counts = {}
    editing_counts = {}
    camera_counts = {}
    art_counts = {}
    sound_counts = {}
    costume_counts = {}

    all_movies = []

    for year in range(1990, max_year):
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
                count_features(country_counts, movie['production_countries'])
                count_features(language_counts, movie['spoken_languages'])
                count_features(cast_counts, movie['cast'])
                count_features(keyword_counts, movie['keywords'])
                count_crew_members(movie['crew'])
                count_month(get_month(movie['release_date']))
                count_original_language(movie['original_language'])
        else:
            print(f'{path} could not be found.')
            exit()
    
    calculate_importances(max_year, 'months', None, month_counts)
    calculate_importances(max_year, 'original_languages', None, original_language_counts)

    calculate_importances(max_year, 'genres', 'genres', genre_counts)
    calculate_importances(max_year, 'companies', 'production_companies', company_counts)
    calculate_importances(max_year, 'countries', 'production_countries', country_counts)
    calculate_importances(max_year, 'languages', 'spoken_languages', language_counts)
    calculate_importances(max_year, 'keywords', 'keywords', keyword_counts)
    calculate_importances(max_year, 'cast', 'cast', cast_counts)

    calculate_importances(max_year, 'directing', 'crew', directing_counts) 
    calculate_importances(max_year, 'writing', 'crew', writing_counts)
    calculate_importances(max_year, 'production', 'crew', production_counts)
    calculate_importances(max_year, 'editing', 'crew', editing_counts)
    calculate_importances(max_year, 'camera', 'crew', camera_counts)
    calculate_importances(max_year, 'art', 'crew', art_counts)
    calculate_importances(max_year, 'sound', 'crew', sound_counts)
    calculate_importances(max_year, 'costume', 'crew', costume_counts)


for feature, impacts in impact_json.items():
    store_impacts_to_csv(feature, impacts)

