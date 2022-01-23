from genericpath import isfile
import json


n_stars = 5

directors = {}
stars = {}
companies = {}


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


def extract(movies):
    for movie in movies:
        date = movie['release_date']
        profit = movie['revenue'] - movie['budget']
        new_credit = {'date': date, 'value': profit}

        for i in range(min(n_stars, len(movie['cast']))):
            update_impact(movie['cast'][i], stars, new_credit)

        for person in movie['crew']:
            if person['job'] == 'Director':
                update_impact(person, directors, new_credit)

        for company in movie['production_companies']:
            update_impact(company, companies, new_credit)


def store(title, values):
    with open(f'data/{title}.json', 'w') as outfile:
        outfile.write(json.dumps(values, indent=4))


for year in range(1990, 2020):
    path = f'data/years/{year}.json'
    if isfile(path):
        movies = json.load(open(path))
        extract(movies)
        store('directors', directors)
        store('stars', stars)
        store('companies', companies)
    else:
        print(f'{path} could not be found.')
