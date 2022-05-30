import os

import pandas as pd
from genericpath import isfile

current_path = os.path.dirname(__file__)
dataset_path = f'{current_path}/../dataset.csv'

def read_dataset():
    if isfile(dataset_path):
        return pd.read_csv(dataset_path)
    else:
        print('Dataset not found')
