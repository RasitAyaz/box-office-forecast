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


directors_json = read_json_file('data/directors.json')
stars_json = read_json_file('data/stars.json')
companies_json = read_json_file('data/companies.json')


def calculate_director_impact(movie):
    director_value_sum = 0
    n_directors = 0

    for person in movie['crew']:
        if person['job'] == 'Director':
            director = directors_json[str(person['id'])]
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
        director = stars_json[str(person['id'])]
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


def calculate_impact(list, json, date):
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


headers = [
    # 'budget',
    # 'director_impact',
    # 'star_impact',
    'company_impact',
    'revenue',
]

with open('data/dataset.csv', 'w', newline='') as dataset:
    writer = csv.writer(dataset)
    writer.writerow(headers)
    for year in range(1990, 2020):
        movies = read_json_file(f'data/years/{year}.json')
        for movie in movies:
            if len(movie['production_companies']) > 0:
                director_impact = 0
                date = movie['release_date']

                directors = [p for p in movie['crew']
                             if p['job'] == 'Director']
                stars = movie['cast'][:5]
                companies = movie['production_companies']

                writer.writerow([
                    # movie['budget'],
                    # calculate_impact(directors, directors_json, date),
                    # calculate_impact(stars, stars_json, date),
                    calculate_impact(companies, companies_json, date),
                    movie['revenue'],
                ])
