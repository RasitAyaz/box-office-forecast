import matplotlib.pyplot as plt
import numpy as np
import json

from numpy.core.fromnumeric import size


years = list(range(1990, 2020))
genres = {}
num_of_films = [0 for _ in range(30)]
box_offices = [[] for _ in range(30)]
runtime_vs_revenue = []
budget_vs_revenue = []


def read_data():
    for year in years:
        index = year - years[0]
        movies = json.load(open(f'data/years/{year}.json'))
        for movie in movies:
            num_of_films[index] += 1
            box_offices[index].append(movie['revenue'])
            runtime_vs_revenue.append((movie['runtime'], movie['revenue']))
            budget_vs_revenue.append((movie['budget'], movie['revenue']))

            for genre in movie['genres']:
                genre_name = genre['name']
                if genre_name not in genres:
                    genres[genre_name] = [0 for _ in range(30)]
                genres[genre_name][index] += 1


def plot_num_of_movies_for_genres():
    for genre, occurrences in genres.items():
        total_occurrence = 0
        for i in occurrences:
            total_occurrence += i
        if total_occurrence > 380:
            plt.plot(years, occurrences, label=genre)
    plt.legend()
    plt.xlabel('year')
    plt.ylabel('# of movies')


def plot_rate_of_movies_for_genres():
    for genre, occurrences in genres.items():
        total_occurrence = 0
        for i in occurrences:
            total_occurrence += i
        if total_occurrence > 380:
            plt.plot(years, np.divide(occurrences, num_of_films), label=genre)
    plt.legend(loc='upper right', bbox_to_anchor=(1.35, 1))
    plt.subplots_adjust(right=0.7)
    plt.xlabel('year')
    plt.ylabel('rate of the movies in a genre')


def plot_box_office_boxplot():
    plt.boxplot(box_offices, flierprops=dict(marker='o', markerfacecolor=(1, 0, 0, 0.25), markeredgecolor='none', markersize=6), showfliers=True)
    plt.xticks(range(1, 31), years, rotation=70)
    plt.xlabel('year')
    plt.ylabel('box office revenue (million $)')


def plot_runtime_vs_revenue():
    for point in runtime_vs_revenue:
        plt.scatter(point[0], point[1], color='green', alpha=0.1, edgecolors='none')
    plt.xlabel('runtime (minutes)')
    plt.ylabel('box office revenue (million $)')


def plot_budget_vs_revenue():
    for point in budget_vs_revenue:
        x = float(point[0]) / 1000000.0
        y = float(point[1]) / 1000000.0
        if x <= 100 and y <= 300:
            plt.scatter(x, y, color='green', alpha=0.1, edgecolors='none', s=10)
    plt.xlabel('budget (million $)')
    plt.ticklabel_format(useOffset=False)
    plt.ylabel('box office revenue (million $)')


read_data()
plot_box_office_boxplot()
plt.show()