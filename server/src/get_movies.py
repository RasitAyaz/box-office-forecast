import json
import os

import requests
from genericpath import isfile

from format_movie_json import format_movie_json

current_path = os.path.dirname(__file__)

tmdb_url = 'https://api.themoviedb.org/3'
tmdb_key = None
keys_path = f'{current_path}/../assets/keys.json'
if isfile(keys_path):
    data = json.load(open(keys_path))
    tmdb_key = data['tmdb_api_key']
else:
    print(f'{keys_path} could not be found.')
    exit()


def get_movie_details_in_page(page_json, movies: dict):
    for movie in page_json['results']:
        if str(movie['id']) in movies:
            continue
        url = f'{tmdb_url}/movie/{movie["id"]}?api_key={tmdb_key}&append_to_response=credits,release_dates,keywords'
        response = requests.get(url)
        if response.ok:
            movie = json.loads(response.text)
            if movie['vote_count'] < 10:
                return False
            if movie['budget'] >= 10000 and movie['revenue'] >= 10000 and movie['belongs_to_collection'] == None:
                print(f'Fetched "{movie["title"]}".')
                movies[movie['id']] = format_movie_json(movie)
        else:
            print(f'{response.status_code}: Could not get "{movie["title"]}".')

    return True

def store_movies(movies, path, year):
    with open(path, 'w') as outfile:
        outfile.write(json.dumps(movies, indent=4))
        print(f'Stored {len(movies)} movies in {year}.json.\n')


def get_movies_by_year(year, init_page_num):
    movies = {}
    path = f'{current_path}/../data/years/{year}.json'
    if init_page_num > 1 and isfile(path):
        movies = json.load(open(path))
    print(f'==================== {year} ====================')
    print(f'Fetching page {init_page_num}...')
    # Release type 3 means theatrical release
    url = f'{tmdb_url}/discover/movie?api_key={tmdb_key}&primary_release_year={year}&with_release_type=3&sort_by=vote_count.desc'
    page_url = f'{url}&page={init_page_num}'
    try:
        response = requests.get(page_url)
        if response.ok:
            init_page = json.loads(response.text)
            total_pages = init_page['total_pages']
            get_movie_details_in_page(init_page, movies)
            store_movies(movies, path, year)
            for page_num in range(init_page_num + 1, total_pages + 1):
                page_url = f'{url}&page={page_num}'
                print(f'Fetching page {page_num}...')
                page_response = requests.get(page_url)
                if page_response.ok:
                    page = json.loads(page_response.text)
                    continue_fetching = get_movie_details_in_page(page, movies)
                    store_movies(movies, path, year)
                    if not continue_fetching:
                        break
                else:
                    print(f'{response.status_code}: Could not get page {page_num}.')
        else:
            print(f'{response.status_code}: Could not get the initial page.')
    except:
        print('ERROR')

    print(f'{len(movies)} movies fetched for the year {year}.')


print('Year: ', end='')
year = int(input())
print('Initial Page: ', end='')
init_page_num = int(input())
get_movies_by_year(year, init_page_num)
