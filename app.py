from flask import Flask, render_template, request, abort
from xtreme.views import xtreme_bp
from samples.views import samples_bp
import requests
from requests.auth import HTTPBasicAuth
from helpers import redis_store
from json import dumps


# app setup
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(samples_bp)
app.register_blueprint(xtreme_bp)


# base views
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sei_redirect')
def sei_redirect():
    confirm_token = request.args.get('confirm_token')
    if not confirm_token:
        abort(400)
    url = app.config['SEI_URL_BASE'] + '/api/integrations/confirm/' + confirm_token
    resp = requests.get(url, auth=HTTPBasicAuth(username=app.config['SEI_ID'], password=app.config['SEI_SECRET']))
    if resp.status_code != 200:
        abort(400)
    data = resp.json()
    redis_store.set(data['exam_id'], dumps(data))
    return render_template('sei_redirect.html')
