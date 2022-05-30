import pandas as pd
from sklearn.preprocessing import StandardScaler


def standardize(data: pd.DataFrame, scaler=StandardScaler()):
    columns = data.columns
    data = scaler.fit_transform(data)
    return pd.DataFrame(data, columns=columns)


def inverse_standardize(data: pd.DataFrame, scaler: StandardScaler):
    columns = data.columns
    data = scaler.inverse_transform(data)
    return pd.DataFrame(data, columns=columns)
