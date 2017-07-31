from flask import Flask, url_for, render_template, request, redirect


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world! Welcome to the example app for external items in SEI!'


@app.route('/get_url/<route>')
def get_url(route):
    return url_for(route, _external=True)


@app.route('/get_url/<route>', methods=['POST'])
def get_url_by_post(route):
    return url_for(route, _external=True)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/everybody_wins', methods=['GET', 'POST'])
def everybody_wins():
    if request.method == 'POST':
        return redirect(url_for('thank_you'))
    return render_template('everybody_wins.html')
