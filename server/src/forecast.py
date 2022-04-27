from genericpath import isfile
import pandas as pd


def use_linear_regression():
    model_path = f'{current_path}/models/linear_regression.csv'

    if isfile(model_path):
        data = pd.read_csv(model_path)
        print(data.iloc[0, 0])


    else:
        print(f'{model_path} could not be found.')


use_linear_regression()