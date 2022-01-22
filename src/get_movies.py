from genericpath import isfile
import requests
import json

api_url = 'https://api.themoviedb.org/3'
api_key = None
keys_path = 'assets/keys.json'
if isfile(keys_path):
    data = json.load(open(keys_path))
    api_key = data['tmdb_api_key']
else:
    print(f'{keys_path} could not be found.')
    exit()


def get_movie_details_in_page(page_json, movies: list):
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
                    'id': movie['id'],
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
                    })
                movies.append(new_movie)
        else:
            print(f'{response.status_code}: Could not get "{movie["title"]}".')

    return True


def get_movies_by_year(year):
    movies = []
    print(f'==================== {year} ====================')
    print(f'Fetching page 1...')
    # Release type 3 means theatrical release
    url = f'{api_url}/discover/movie?api_key={api_key}&primary_release_year={year}&with_release_type=3&sort_by=vote_count.desc'
    response = requests.get(url)
    if response.ok:
        first_page = json.loads(response.text)
        total_pages = first_page['total_pages']
        get_movie_details_in_page(first_page, movies)
        for page_num in range(2, total_pages + 1):
            page_url = f'{url}&page={page_num}'
            print(f'Fetching page {page_num}...')
            page_response = requests.get(page_url)
            if page_response.ok:
                page = json.loads(page_response.text)
                continue_fetching = get_movie_details_in_page(page, movies)
                if not continue_fetching:
                    break
            else:
                print(f'{response.status_code}: Could not get page {page_num}.')
    else:
        print(f'{response.status_code}: Could not get the first page.')

    print(f'{len(movies)} movies fetched for the year {year}.')
    filename = f'data/years/{year}.json'
    with open(filename, 'w') as outfile:
        print(f'Storing movies in {filename}...')
        outfile.write(json.dumps(movies, indent=4))
        print('Successful.')


print('Year: ', end='')
year = int(input())
get_movies_by_year(year)
