from genericpath import isfile
import os


import seaborn as sns
import pandas as pd

import matplotlib.pyplot as mp


current_path = os.path.dirname(__file__)

dataset_path = f'{current_path}/../dataset.csv'


if isfile(dataset_path):

    data = pd.read_csv(dataset_path)

    print(f'Data size: {len(data)}')
    

df = data.copy()

X = df.drop("revenue", axis=1)

y = df["revenue"]


Var_Corr = df.corr()

sns.heatmap(Var_Corr, xticklabels=Var_Corr.columns, yticklabels=Var_Corr.columns, annot=True)

#mp.show()



dataset_path = f'{current_path}/../data/impacts/genres.csv'


if isfile(dataset_path):

    df_genres = pd.read_csv(dataset_path)
    df_genres = df_genres[:10]
    print(f'Data size: {len(data)}')


genre_data = df_genres["name"]

importance_data = df_genres["importance"]

colors = ["#3B1A1F", "#0F6CC5", "#D46DDE", "#F5A86C", "#E1EB67"]


mp.pie(importance_data, labels=genre_data, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

mp.title("İmportance of Genres")

mp.show()