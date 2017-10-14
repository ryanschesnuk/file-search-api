from flask import Flask

from resources.occurrences import occurrences_api

DEBUG = True
HOST = "127.0.0.1"
PORT = 8000

app = Flask(__name__)
app.register_blueprint(occurrences_api, url_prefix='/api/v1/search')

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
