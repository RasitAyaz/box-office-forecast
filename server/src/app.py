from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)


@app.route('/movies', methods=['GET'])
def index():
    response = jsonify({"test": ["test1", "test2"]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
