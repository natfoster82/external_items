from flask import Blueprint, url_for, render_template, request, redirect, jsonify, abort, current_app
import requests
from requests.auth import HTTPBasicAuth
from helpers import get_integration_info


samples_bp = Blueprint('samples', __name__, template_folder='templates', static_folder='static', url_prefix='/samples')


@samples_bp.route('/get_url/<route>')
def get_url(route):
    return url_for(route, _external=True, **request.args)


@samples_bp.route('/get_url/<route>', methods=['POST'])
def get_url_by_post(route):
    data = request.get_json() or {}
    return url_for(route, _external=True, **data)


@samples_bp.route('/get_url_secure/<route>')
def get_url_secure(route):
    needed_api_token = current_app.config['api_token']
    given_api_token = request.args.get('api_token')
    if given_api_token != needed_api_token:
        return jsonify(), 404
    request.args.pop('api_token')
    return url_for(route, _external=True, **request.args)


@samples_bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')


@samples_bp.route('/adventure')
def adventure():
    return render_template('adventure.html')


@samples_bp.route('/connect4')
def connect4():
    return render_template('c4.html')


@samples_bp.route('/colorblind', methods=['GET', 'POST'])
def colorblind():
    if request.method == 'POST':
        response_id = request.args.get('response_id')
        if response_id:
            exam_id = request.args.get('exam_id')
            external_token = request.args.get('external_token')
            url = current_app.config['SEI_URL_BASE'] + '/api/set_response/' + response_id
            json = {
                'value': request.form['submit']
            }
            if external_token:
                url += '?external_token=' + external_token
                r = requests.post(url, json=json)
            elif exam_id:
                try:
                    integration_info = get_integration_info(exam_id)
                except ValueError:
                    abort(400)
                token = integration_info['token']
                headers = {
                    'Authorization': 'Bearer {0}'.format(token)
                }
                r = requests.post(url, json=json, headers=headers)
            else:
                r = None
            if r and r.status_code not in {200, 201}:
                abort(400)
        return redirect(url_for('samples.thank_you'))
    return render_template('colorblind.html', query_params=request.args)
