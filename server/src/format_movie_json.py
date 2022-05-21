def format_movie_json(movie):
    new_movie = {
        'imdb_id': movie['imdb_id'],
        'title': movie['title'],
        'original_language': movie['original_language'],
        'overview': movie['overview'],
        'budget': movie['budget'],
        'revenue': movie['revenue'],
        'release_date': movie['release_date'],
        'runtime': movie['runtime'],
        'popularity': movie['popularity'],
        'vote_average': movie['vote_average'],
        'vote_count': movie['vote_count'],
        'genres': movie['genres'],
        'production_companies': movie['production_companies'],
        'production_countries': movie['production_countries'],
        'spoken_languages': movie['spoken_languages'],
        'keywords': movie['keywords']['keywords'],
        'release_dates': movie['release_dates']['results'],
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

    return new_movie
