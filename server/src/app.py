import json
import os

import requests
from flask import Flask, jsonify, render_template, request
from flask_script import Manager
from genericpath import isfile

from forecast import forecast_with_linear_regression

current_path = os.path.dirname(__file__)
app = Flask(__name__)
manager = Manager(app)

tmdb_url = 'https://api.themoviedb.org/3'
tmdb_key = None

@app.route('/movies', methods=['GET'])
def index():
    response = jsonify({"test": ["test1", "test2"]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/forecast', methods=['GET'])
def forecast():
    movie_id = request.args.get('movie_id')
    url = f'{tmdb_url}/movie/{movie_id}?api_key={tmdb_key}&append_to_response=credits,release_dates,keywords'
    tmdb_response = requests.get(url)
    lr = None
    print(tmdb_key)
    if tmdb_response.ok:
        movie = json.loads(tmdb_response.text)
        lr = forecast_with_linear_regression(movie)
    else:
        print(f'{tmdb_response.status_code}: Could not get movie with id {movie_id}.')
        print(tmdb_response.text)
    response = jsonify({
        'linear_regression': lr
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def init():
    keys_path = f'{current_path}/../assets/keys.json'
    if isfile(keys_path):
        data = json.load(open(keys_path))
        global tmdb_key
        tmdb_key = data['tmdb_api_key']
    else:
        print(f'{keys_path} could not be found.')
        exit()

@manager.command
def runserver():
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    init()
    print(tmdb_key)

if __name__ == '__main__':
    manager.run()
