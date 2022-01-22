import csv
from datetime import datetime
from genericpath import isfile
import json


def read_json_file(path):
    if isfile(path):
        return json.load(open(path))
    else:
        print(f'{path} could not be found.')
        exit()


directors = read_json_file('data/directors.json')
stars = read_json_file('data/stars.json')


def calculate_director_impact(movie):
    director_value_sum = 0
    n_directors = 0

    for person in movie['crew']:
        if person['job'] == 'Director':
            director = directors[str(person['id'])]
            value_sum = 0
            n_credits = 0
            for credit in director['credits']:
                if credit['date'] > movie['release_date']:
                    break
                value_sum += credit['value']
                n_credits += 1

            director_value_sum += value_sum / n_credits
            n_directors += 1

    return director_value_sum / n_directors


def calculate_star_impact(movie):
    star_value_sum = 0
    n_stars = 0

    for i in range(min(5, len(movie['cast']))):
        person = movie['cast'][i]
        director = stars[str(person['id'])]
        value_sum = 0
        n_credits = 0
        for credit in director['credits']:
            if credit['date'] > movie['release_date']:
                break
            value_sum += credit['value']
            n_credits += 1

        star_value_sum += value_sum / n_credits
        n_stars += 1

    return star_value_sum / n_stars


headers = [
    'budget',
    'director_impact',
    'star_impact',
    'revenue',
]

with open('data/dataset.csv', 'w', newline='') as dataset:
    writer = csv.writer(dataset)
    writer.writerow(headers)
    for year in range(1990, 2020):
        movies = read_json_file(f'data/years/{year}.json')
        for movie in movies:
            director_impact = 0
            writer.writerow([
                movie['budget'],
                calculate_director_impact(movie),
                calculate_star_impact(movie),
                movie['revenue'],
            ])
