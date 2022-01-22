import json


years = list(range(1990, 2020))

count = {}
count['total'] = 0

for year in years:
    index = year - years[0]
    movies = json.load(open(f'data/years/{year}.json'))
    count['total'] += len(movies)
    for movie in movies:
        for feature in ['budget', 'revenue', 'genres', 'runtime', 'production_countries', 'production_companies', 'imdb_id']:
            if feature not in count:
                count[feature] = 0
            if movie[feature] is not None:
                count[feature] += 1

print(count)
