from flask import Flask


DEBUG = True
HOST = "127.0.0.1"
PORT = 8000

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
