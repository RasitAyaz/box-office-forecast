from genericpath import isfile
import json
import os
import pandas as pd
from scipy.stats import pearsonr

current_path = os.path.dirname(__file__)


def calculate_correlation(data):
    x = data['star_impact']
    y = data['revenue']
    x.corr(y, method='spearman')
    test_stats, p_value = pearsonr(x, y)
    print(f'{test_stats}, {p_value}')


dataset_path = f'{current_path}/../dataset.csv'

if isfile(dataset_path):
    print('Reading dataset...')
    data = pd.read_csv(dataset_path)
    print(f'Data size: {len(data)}')
    calculate_correlation(data)
else:
    print(f'{dataset_path} could not be found.')
