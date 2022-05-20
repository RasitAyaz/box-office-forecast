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


def read_impact_csv(feature):
    path = f'{data_path}/impacts/{feature}.csv'
    return pd.read_csv(path)


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


month_impacts = read_impact_csv('months')
original_language_impacts = read_impact_csv('original_languages')

genre_impacts = read_impact_csv('genres')
company_impacts = read_impact_csv('companies')
country_impacts = read_impact_csv('countries')
language_impacts = read_impact_csv('languages')
cast_impacts = read_impact_csv('cast')
keyword_impacts = read_impact_csv('keywords')

directing_impacts = read_impact_csv('directing')
writing_impacts = read_impact_csv('writing')
production_impacts = read_impact_csv('production')
editing_impacts = read_impact_csv('editing')
camera_impacts = read_impact_csv('camera')
art_impacts = read_impact_csv('art')
sound_impacts = read_impact_csv('sound')
costume_impacts = read_impact_csv('costume')


data_items = []

for year in range(1990, 2020):
    print(f'Processing year {year}...', end='\r')
    movies: dict
    movies = read_json_file(f'{current_path}/../data/years/{year}.json')
    for id, movie in movies.items():
        date = movie['release_date']

        crew = movie['crew']
        directing = [p for p in crew if p['department'] == 'Directing']
        writing = [p for p in crew if p['department'] == 'Writing']
        production = [p for p in crew if p['department'] == 'Production']
        editing = [p for p in crew if p['department'] == 'Editing']
        camera = [p for p in crew if p['department'] == 'Camera']
        art = [p for p in crew if p['department'] == 'Art']
        sound = [p for p in crew if p['department'] == 'Sound']
        costume = [p for p in crew if p['department'] == 'Costume & Make-Up']

        cast = movie['cast'][:5]
        companies = movie['production_companies']

        genres = movie['genres']

        if len(cast) == 0 or len(crew) == 0 or len(companies) == 0 or len(genres) == 0:
            continue

        month_impact = get_impact(get_month(date), month_impacts)
        original_language_impact = get_impact(movie['original_language'], original_language_impacts)

        genre_avg, genre_max = get_list_impact(genres, genre_impacts)
        company_avg, company_max = get_list_impact(companies, company_impacts)
        country_avg, country_max = get_list_impact(movie['production_countries'], country_impacts)
        language_avg, language_max = get_list_impact(movie['spoken_languages'], language_impacts)
        cast_avg, cast_max = get_list_impact(cast, cast_impacts)
        keyword_avg, keyword_max = get_list_impact(movie['keywords'], keyword_impacts)

        director_avg, director_max = get_list_impact(directing, directing_impacts)
        writer_avg, writer_max = get_list_impact(writing, writing_impacts)
        producer_avg, producer_max = get_list_impact(production, production_impacts)
        editor_avg, editor_max = get_list_impact(editing, editing_impacts)
        camera_avg, camera_max = get_list_impact(camera, camera_impacts)
        art_avg, art_max = get_list_impact(art, art_impacts)
        sound_avg, sound_max = get_list_impact(sound, sound_impacts)
        costume_avg, costume_max = get_list_impact(costume, costume_impacts)


        if len(companies) > 0 and len(genres) > 0:
            data_items.append({
                'budget': movie['budget'],
                'runtime': movie['runtime'],
                'month_impact': month_impact,
                'original_language_impact': original_language_impact,
                'genre_avg': genre_avg,
                'genre_max': genre_max,
                'company_avg': company_avg,
                'company_max': company_max,
                'country_avg': country_avg,
                'country_max': country_max,
                'language_avg': language_avg,
                'language_max': language_max,
                'cast_avg': cast_avg,
                'cast_max': cast_max,
                'keyword_avg': keyword_avg,
                'keyword_max': keyword_max,
                'director_avg': director_avg,
                'director_max': director_max,
                'writer_avg': writer_avg,
                'writer_max': writer_max,
                'producer_avg': producer_avg,
                'producer_max': producer_max,
                'editor_avg': editor_avg,
                'editor_max': editor_max,
                'camera_avg': camera_avg,
                'camera_max': camera_max,
                'art_avg': art_avg,
                'art_max': art_max,
                'sound_avg': sound_avg,
                'sound_max': sound_max,
                'costume_avg': costume_avg,
                'costume_max': costume_max,
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
