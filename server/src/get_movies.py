from genericpath import isfile
import os
import requests
import json

current_path = os.path.dirname(__file__)

api_url = 'https://api.themoviedb.org/3'
api_key = None
keys_path = f'{current_path}/../assets/keys.json'
if isfile(keys_path):
    data = json.load(open(keys_path))
    api_key = data['tmdb_api_key']
else:
    print(f'{keys_path} could not be found.')
    exit()


def get_movie_details_in_page(page_json, movies: dict):
    for movie in page_json['results']:
        url = f'{api_url}/movie/{movie["id"]}?api_key={api_key}&append_to_response=credits'
        response = requests.get(url)
        if response.ok:
            movie = json.loads(response.text)
            if movie['vote_count'] < 10:
                return False
            if movie['budget'] > 0 and movie['revenue'] > 0 and movie['belongs_to_collection'] == None:
                print(f'Fetched "{movie["title"]}".')
                new_movie = {
                    'imdb_id': movie['imdb_id'],
                    'title': movie['title'],
                    'overview': movie['overview'],
                    'budget': movie['budget'],
                    'revenue': movie['revenue'],
                    'popularity': movie['popularity'],
                    'release_date': movie['release_date'],
                    'runtime': movie['runtime'],
                    'genres': movie['genres'],
                    'production_companies': movie['production_companies'],
                    'production_countries': movie['production_countries'],
                    'cast': [],
                    'crew': [],
                }
                for person in movie['credits']['cast']:
                    new_movie['cast'].append({
                        'id': person['id'],
                        'name': person['name'],
                        'character': person['character'],
                    })
                for person in movie['credits']['crew']:
                    new_movie['crew'].append({
                        'id': person['id'],
                        'name': person['name'],
                        'job': person['job'],
                        'department': person['department'],
                    })
                movies[movie['id']] = new_movie
        else:
            print(f'{response.status_code}: Could not get "{movie["title"]}".')

    return True

def store_movies(movies, path):
    with open(path, 'w') as outfile:
        outfile.write(json.dumps(movies, indent=4))
        print(f'Stored {len(movies)} movies in {path}...\n')


def get_movies_by_year(year, init_page_num):
    movies = {}
    path = f'{current_path}/../data/years/{year}.json'
    if init_page_num > 1 and isfile(path):
        movies = json.load(open(path))
    print(f'==================== {year} ====================')
    print(f'Fetching page {init_page_num}...')
    # Release type 3 means theatrical release
    url = f'{api_url}/discover/movie?api_key={api_key}&primary_release_year={year}&with_release_type=3&sort_by=vote_count.desc'
    page_url = f'{url}&page={init_page_num}'
    response = requests.get(page_url)
    if response.ok:
        init_page = json.loads(response.text)
        total_pages = init_page['total_pages']
        get_movie_details_in_page(init_page, movies)
        store_movies(movies, path)
        for page_num in range(init_page_num + 1, total_pages + 1):
            page_url = f'{url}&page={page_num}'
            print(f'Fetching page {page_num}...')
            page_response = requests.get(page_url)
            if page_response.ok:
                page = json.loads(page_response.text)
                continue_fetching = get_movie_details_in_page(page, movies)
                store_movies(movies, path)
                if not continue_fetching:
                    break
            else:
                print(f'{response.status_code}: Could not get page {page_num}.')
    else:
        print(f'{response.status_code}: Could not get the initial page.')

    print(f'\n{len(movies)} movies fetched for the year {year}.')


print('Year: ', end='')
year = int(input())
print('Initial Page: ', end='')
init_page_num = int(input())
get_movies_by_year(year, init_page_num)
