import os

import pandas as pd

current_path = os.path.dirname(__file__)
data_path = f'{current_path}/../data'


def read_impact_csv(feature):
    path = f'{data_path}/impacts/{feature}.csv'
    return pd.read_csv(path)


def read_impacts():
    return {
        'months': read_impact_csv('months'),
        'original_languages': read_impact_csv('original_languages'),

        'genres': read_impact_csv('genres'),
        'companies': read_impact_csv('companies'),
        'countries': read_impact_csv('countries'),
        'languages': read_impact_csv('languages'),
        'keywords': read_impact_csv('keywords'),
        'cast': read_impact_csv('cast'),

        'directing': read_impact_csv('directing'),
        'writing': read_impact_csv('writing'),
        'production': read_impact_csv('production'),
        'editing': read_impact_csv('editing'),
        'camera': read_impact_csv('camera'),
        'art': read_impact_csv('art'),
        'sound': read_impact_csv('sound'),
        'costume': read_impact_csv('costume')
    }
