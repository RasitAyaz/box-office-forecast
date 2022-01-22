from genericpath import isfile
import json


directors = {}
stars = {}


def update_director(director, date, value):
    id = director['id']
    new_credit = {
        'date': date,
        'value': value,
    }
    if id not in directors:
        directors[id] = {
            'name': director['name'],
            'credits': [new_credit],
        }
    else:
        credits: list = directors[id]['credits']
        for index, credit in enumerate(credits):
            if new_credit['date'] < credit['date']:
                credits.insert(index, new_credit)
                return
        credits.append(new_credit)


def update_star(star, date, value):
    id = star['id']
    new_credit = {
        'date': date,
        'value': value,
    }
    if id not in stars:
        stars[id] = {
            'name': star['name'],
            'credits': [new_credit],
        }
    else:
        credits: list = stars[id]['credits']
        for index, credit in enumerate(credits):
            if new_credit['date'] < credit['date']:
                credits.insert(index, new_credit)
                return
        credits.append(new_credit)


def extract(movies):
    for movie in movies:
        profit = movie['revenue'] - movie['budget']
        date = movie['release_date']
        for i in range(min(5, len(movie['cast']))):
            update_star(movie['cast'][i], date, profit)
        for person in movie['crew']:
            if person['job'] == 'Director':
                update_director(person, date, profit)


def store():
    with open('data/directors.json', 'w') as outfile:
        outfile.write(json.dumps(directors, indent=4))
    with open('data/stars.json', 'w') as outfile:
        outfile.write(json.dumps(stars, indent=4))


for year in range(1990, 2020):
    path = f'data/years/{year}.json'
    if isfile(path):
        movies = json.load(open(path))
        extract(movies)
        store()
    else:
        print(f'{path} could not be found.')
