from genericpath import isfile
import json
import pandas as pd
from scipy.stats.stats import pearsonr


def count_non_null_data():
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


def calculate_correlation(data):
    x = data['company_impact']
    y = data['revenue']
    x.corr(y, method='spearman')
    test_stats, p_value = pearsonr(x, y)
    print('%.4f, %.4f' % (test_stats, p_value))


dataset_path = 'data/dataset.csv'

if isfile(dataset_path):
    print('Reading dataset...')
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')
    calculate_correlation(data)
else:
    print(f'{dataset_path} could not be found.')
