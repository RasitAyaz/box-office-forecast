from genericpath import isfile
import json
import os
from statistics import mean

current_path = os.path.dirname(__file__)

n_stars = 5
n_genres = 1

directors_out = {}
stars_out = {}
companies_out = {}
genres_out = {}


def add_credit(credits: list, new_credit):
    for index, credit in enumerate(credits):
        if new_credit['date'] < credit['date']:
            credits.insert(index, new_credit)
            return
    credits.append(new_credit)


def update_impact(item, items, new_credit):
    id = item['id']
    if id not in items:
        items[id] = {'name': item['name'], 'credits': [new_credit]}
    else:
        add_credit(items[id]['credits'], new_credit)


def add_genre_value(genre, new_value):
    id = genre['id']
    if id not in genres_out:
        genres_out[id] = {'name': genre['name'], 'values': [new_value]}
    else:
        if 'values' not in genres_out[id]:
            print(genre)
        genres_out[id]['values'].append(new_value)


def extract(movies: dict):
    for id, movie in movies.items():
        date = movie['release_date']
        profit = movie['revenue'] - movie['budget']
        new_credit = {'date': date, 'value': profit}

        for i in range(min(n_stars, len(movie['cast']))):
            update_impact(movie['cast'][i], stars_out, new_credit)

        for person in movie['crew']:
            if person['job'] == 'Director':
                update_impact(person, directors_out, new_credit)

        for company in movie['production_companies']:
            update_impact(company, companies_out, new_credit)

        for genre in movie['genres'][:n_genres]:
            add_genre_value(genre, profit)


def calculate_genre_values():
    for id, genre in genres_out.items():
        genre: dict
        values: list = genre['values']
        genre['value'] = mean(values)
        genre.pop('values')


def store(title, values):
    with open(f'{current_path}/../data/{title}.json', 'w') as outfile:
        outfile.write(json.dumps(values, indent=4))


for year in range(1990, 2020):
    path = f'{current_path}/../data/years/{year}.json'
    if isfile(path):
        movies_of_year = json.load(open(path))
        extract(movies_of_year)
    else:
        print(f'{path} could not be found.')
        exit()

calculate_genre_values()

store('directors', directors_out)
store('stars', stars_out)
store('companies', companies_out)
store('genres', genres_out)
