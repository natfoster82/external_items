from flask import Flask, url_for, render_template, request, redirect, jsonify


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, world! Welcome to the example app for external items in SEI!'


@app.route('/get_url/<route>')
def get_url(route):
    return url_for(route, **request.args, _external=True)


@app.route('/get_url/<route>', methods=['POST'])
def get_url_by_post(route):
    data = request.get_json()
    return url_for(route, **data, _external=True)


@app.route('/get_url_secure/<route>')
def get_url_secure(route):
    needed_api_token = app.config['api_token']
    given_api_token = request.args.get('api_token')
    if given_api_token != needed_api_token:
        return jsonify(), 404
    request.args.pop('api_token')
    return url_for(route, **request.args, _external=True)


@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@app.route('/everybody_wins', methods=['GET', 'POST'])
def everybody_wins():
    if request.method == 'POST':
        request_id = request.args.get('request_id')
        if request_id:
            # call the SEI webhook
            pass
        return redirect(url_for('thank_you'))
    return render_template('everybody_wins.html')
