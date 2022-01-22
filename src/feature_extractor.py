from genericpath import isfile
import json


directors = {}
stars = {}


def update_director(director, date, value):
    id = director['id']
    if id not in directors:
        directors[id] = {
            'name': director['name'],
            'credits': [],
        }
    credits: list = directors[id]['credits']
    credits.append({
        'date': date,
        'value': value,
    })


def extract(movies):
    for movie in movies:
        profit = movie['revenue'] - movie['budget']
        for person in movie['crew']:
            if person['job'] == 'Director':
                update_director(person, movie['release_date'], profit)


def store():
    with open('data/directors.json', 'w') as outfile:
        outfile.write(json.dumps(directors, indent=4))


for year in range(1990, 2020):
    path = f'data/years/{year}.json'
    if isfile(path):
        movies = json.load(open(path))
        extract(movies)
        store()
    else:
        print(f'{path} could not be found.')
