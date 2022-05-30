import json
import os
from tkinter.tix import WINDOW

import pandas as pd
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from genericpath import isfile
from numpy import ndarray
from sklearn.preprocessing import StandardScaler

from forecast import forecast_linear_regression
from format_movie_json import format_movie_json
from movie_to_vector import movie_to_vector
from read_dataset import read_dataset
from read_impacts import read_impacts
from standardization import inverse_standardize, standardize

load_dotenv()
app = Flask(__name__)
current_path = os.path.dirname(__file__)


def tmdb_url():
    return os.getenv('TMDB_URL')

def tmdb_key():
    return os.getenv('TMDB_KEY')


@app.route('/movies', methods=['GET'])
def index():
    response = jsonify({"test": ["test1", "test2"]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/forecast', methods=['GET'])
def forecast():
    movie_id = request.args.get('movie_id')
    url = f'{tmdb_url()}/movie/{movie_id}?api_key={tmdb_key()}&append_to_response=credits,release_dates,keywords'
    tmdb_response = requests.get(url)
    lr: ndarray
    if tmdb_response.ok:
        movie_json = json.loads(tmdb_response.text)
        movie = movie_to_vector(format_movie_json(movie_json), read_impacts(), include_revenue=False)
        data = read_dataset()

        X = data.drop('revenue', axis=1)
        y = data['revenue']

        # Adding new movie to the dataset
        X.loc[len(X)] = movie

        pd.set_option('display.max_columns', 100)

        X = X.fillna(X.mean())
        X = standardize(X)
        
        lr = forecast_linear_regression(X.tail(1))

        # Inverse standardization
        lr = lr * y.std() + y.mean()
        print(lr)

        # Adding standardized forecast value and applying inverse standardization
        # scaler = StandardScaler()
        # y = standardize(y, scaler)
        # y.loc[len(X)] = {'revenue': lr}
        # y = inverse_standardize(y, scaler)
        # lr = y.tail(1).iloc[0]['revenue']
    else:
        print(f'{tmdb_response.status_code}: Could not get movie with id {movie_id}.')
    response = jsonify({
        'linear_regression': lr
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
