from genericpath import isfile
import os

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as mp


# Plotting Heat Map
def plot_heatmap():

    dataset_path = f'{current_path}/../dataset.csv'
    data = data_read_from(dataset_path)

    target_Var = ["budget", "genre_max", "company_max", "language_max", "cast_max",
                  "keyword_max", "directing_max", "writing_max", "production_max",
                  "editing_max", "camera_max", "art_max", "sound_max", "costume_max",
                  "revenue"]

    df = data[target_Var].copy()
    Var_Corr = df.corr()

    mp.subplots(figsize=(19.2, 10.8), dpi=150)

    sns.heatmap(Var_Corr, xticklabels=Var_Corr.columns, yticklabels=Var_Corr.columns,
                annot=True, fmt='.2f', cmap="YlOrRd", vmin=0, vmax=1)
    mp.title('Correlation between variables')
    mp.xlabel('Variables')
    mp.ylabel('Variables')
    mp.savefig(f'{current_path}/../figures/Correlation_between_variables.jpg')
    mp.show()


def plot_scatter_matrix(data):
    sns.set(style="ticks")
    sns.pairplot(data, hue="revenue", palette="husl", height=2.5, plot_kws={
                 "s": 10}, diag_kind="kde", diag_kws={"shade": True})
    mp.savefig(f'{current_path}/../figures/Scatter_matrix.jpg')
    mp.show()


def plot_box_plot():

    impact_genres_path = f'{current_path}/../data/impacts/genres.csv'
    data = data_read_from(impact_genres_path)
    data = data[:10]

    mp.rcdefaults()
    fig, ax = mp.subplots(figsize=(19.2, 10.8), dpi=150)

    ax.barh(data['name'], data['importance'], color='#354259', align='center')
    ax.set_yticks(data['name'])
    ax.invert_yaxis()
    ax.set_xlabel('Genres')
    ax.set_title('Impacts of Genres')
    mp.savefig(f'{current_path}/../figures/Impacts_of_Genres.jpg')
    mp.show()


def data_read_from(path):
    if isfile(path):
        return pd.read_csv(path)
    else:
        print(f'{path} could not be found.')
        exit()


current_path = os.path.dirname(__file__)

# plot_heatmap()
plot_box_plot()
