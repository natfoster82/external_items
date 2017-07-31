from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world! Welcome to the example app for external items in SEI!'