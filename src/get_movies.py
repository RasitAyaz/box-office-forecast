from genericpath import isfile
import requests
import json

api_url = 'https://api.themoviedb.org/3'
api_key = None
keys_path = 'assets/keys.json'
if isfile(keys_path):
    file = open(keys_path)
    data = json.load(file)
    api_key = data['tmdb_api_key']
else:
    print(f'{keys_path} could not be found.')
    exit()

movies = []


def get_movie_details_in_page(page_json):
    for movie in page_json['results']:
        url = f'{api_url}/movie/{movie["id"]}?api_key={api_key}'
        response = requests.get(url)
        if response.ok:
            movie = json.loads(response.text)
            if movie['vote_count'] < 10:
                return False
            if movie['budget'] > 0 and movie['revenue'] > 0 and movie['belongs_to_collection'] == None:
                print(f'Fetched "{movie["title"]}".')
                movies.append(movie)
        else:
            print(f'{response.status_code}: Could not get "{movie["title"]}".')

    return True


def get_movies_by_year(year):
    print(f'==================== {year} ====================')
    print(f'Fetching page 1...')
    url = f'{api_url}/discover/movie?api_key={api_key}&primary_release_year={year}&sort_by=vote_count.desc'
    response = requests.get(url)
    if response.ok:
        first_page = json.loads(response.text)
        total_pages = first_page['total_pages']
        get_movie_details_in_page(first_page)
        for page_num in range(2, total_pages + 1):
            page_url = f'{url}&page={page_num}'
            print(f'Fetching page {page_num}...')
            page_response = requests.get(page_url)
            if page_response.ok:
                page = json.loads(page_response.text)
                continue_fetching = get_movie_details_in_page(page)
                if not continue_fetching:
                    break
            else:
                print(f'{response.status_code}: Could not get page {page_num}.')
    else:
        print(f'{response.status_code}: Could not get the first page.')

    print(f'{len(movies)} movies fetched for the year {year}.')
    filename = f'data/{year}.json'
    with open(filename, 'w') as outfile:
        print(f'Storing movies in {filename}...')
        outfile.write(json.dumps(movies, indent=4))
        print('Successful.')


for year in range(1990, 2020):
    get_movies_by_year(year)
