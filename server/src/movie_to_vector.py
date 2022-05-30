import pandas as pd


def get_id(item):
    if 'iso_3166_1' in item:
        return item['iso_3166_1']
    if 'iso_639_1' in item:
        return item['iso_639_1']
    return item['id']


def get_name(item):
    if 'english_name' in item:
        return item['english_name']
    return item['name']


def get_year(date):
    return int(date[0:4])


def get_month(date):
    return int(date[5:7])


def get_impact(year, id, impact_data: pd.DataFrame):
    search_data = impact_data.loc[impact_data['id'] == id]
    if len(search_data) == 0:
        return None
    else:
        return search_data.iloc[0][year]


def get_list_impact(year, list, impact_data):
    impact_max = 0
    impact_sum = 0

    for item in list:
        impact = get_impact(year, get_id(item), impact_data)
        if impact is None:
            continue
        impact_sum += impact
        impact_max = max(impact_max, impact)

    if len(list) == 0 or impact_max == 0:
        return pd.NA, pd.NA
    else:
        impact_avg = impact_sum / len(list)
        return impact_avg, impact_max


def get_diminishing_list_impact(year, list, impact_data):
    order = 1
    impact_sum = 0
    weight_sum = 0

    for item in list:
        impact = get_impact(year, get_id(item), impact_data)
        if impact is None:
            continue
        weight = 1 / order
        impact = impact * weight
        order += 1
        impact_sum += impact
        weight_sum += weight

    if weight_sum == 0:
        return pd.NA
    else:
        return impact_sum


def movie_to_vector(movie, impacts, include_revenue=True):
    date = movie['release_date']
    year = get_year(date)

    crew = movie['crew']
    cast = movie['cast']
    companies = movie['production_companies']
    genres = movie['genres']

    if len(cast) == 0 or len(crew) == 0 or len(companies) == 0 or len(genres) == 0:
        return None

    directing = [p for p in crew if p['department'] == 'Directing']
    writing = [p for p in crew if p['department'] == 'Writing']
    production = [p for p in crew if p['department'] == 'Production']
    editing = [p for p in crew if p['department'] == 'Editing']
    camera = [p for p in crew if p['department'] == 'Camera']
    art = [p for p in crew if p['department'] == 'Art']
    sound = [p for p in crew if p['department'] == 'Sound']
    costume = [p for p in crew if p['department'] == 'Costume & Make-Up']

    month_impact = get_impact(year, get_month(date), impacts['months'])
    original_language_impact = get_impact(year, movie['original_language'], impacts['original_languages'])

    genre_avg, genre_max = get_list_impact(year, genres, impacts['genres'])
    company_avg, company_max = get_list_impact(year, companies, impacts['companies'])
    country_avg, country_max = get_list_impact(year, movie['production_countries'], impacts['countries'])
    language_avg, language_max = get_list_impact(year, movie['spoken_languages'], impacts['languages'])
    cast_avg, cast_max = get_list_impact(year, cast, impacts['cast'], str(int(date[0:4]) - 1))
    cast_dim = get_diminishing_list_impact(year, cast, impacts['cast'], str(int(date[0:4]) - 1))
    keyword_avg, keyword_max = get_list_impact(year, movie['keywords'], impacts['keywords'])
    keyword_dim = get_diminishing_list_impact(year, movie['keywords'], impacts['keywords'])

    directing_avg, directing_max = get_list_impact(year, directing, impacts['directing'])
    writing_avg, writing_max = get_list_impact(year, writing, impacts['writing'])
    production_avg, production_max = get_list_impact(year, production, impacts['production'])
    editing_avg, editing_max = get_list_impact(year, editing, impacts['editing'])
    camera_avg, camera_max = get_list_impact(year, camera, impacts['camera'])
    art_avg, art_max = get_list_impact(year, art, impacts['art'])
    sound_avg, sound_max = get_list_impact(year, sound, impacts['sound'])
    costume_avg, costume_max = get_list_impact(year, costume, impacts['costume'])

    vector = {
        'budget': movie['budget'],
        'runtime': movie['runtime'],
        'month_impact': month_impact,
        'original_language_impact': original_language_impact,
        'genre_avg': genre_avg,
        'genre_max': genre_max,
        'company_avg': company_avg,
        'company_max': company_max,
        'country_avg': country_avg,
        'country_max': country_max,
        'language_avg': language_avg,
        'language_max': language_max,
        'cast_avg': cast_avg,
        'cast_max': cast_max,
        'cast_dim': cast_dim,
        'cast_count': len(cast),
        'keyword_avg': keyword_avg,
        'keyword_max': keyword_max,
        'keyword_dim': keyword_dim,
        'keyword_count': len(movie['keywords']),
        'directing_avg': directing_avg,
        'directing_max': directing_max,
        'writing_avg': writing_avg,
        'writing_max': writing_max,
        'production_avg': production_avg,
        'production_max': production_max,
        'editing_avg': editing_avg,
        'editing_max': editing_max,
        'camera_avg': camera_avg,
        'camera_max': camera_max,
        'art_avg': art_avg,
        'art_max': art_max,
        'sound_avg': sound_avg,
        'sound_max': sound_max,
        'costume_avg': costume_avg,
        'costume_max': costume_max,
    }

    if include_revenue:
        vector['revenue'] = movie['revenue']

    return vector
