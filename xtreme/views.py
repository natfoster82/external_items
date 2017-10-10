from flask import Blueprint, request, current_app, render_template, url_for, abort
import requests
from requests.auth import HTTPBasicAuth
from itsdangerous import BadSignature, SignatureExpired
from helpers import redis_store, external_serializer


xtreme_bp = Blueprint('xtreme', __name__, template_folder='templates', static_folder='static', url_prefix='/xtreme')


@xtreme_bp.route('/get_url/<lab_id>')
def get_url(lab_id):
    response_id = request.args.get('response_id')
    instance_id = redis_store.get(response_id)
    token = external_serializer.dumps([lab_id, instance_id])
    return url_for('xtreme.lab', token=token)


@xtreme_bp.route('/<token>')
def lab(token):
    try:
        lab_id, instance_id = external_serializer.loads(token, max_age=60)
    except (BadSignature, SignatureExpired):
        abort(400)

    response_id = request.args.get('response_id')
    if not response_id:
        abort(400)
    url_base = '{0}/labapiConnection/ShowLab?labInstanceGuid={1}&fullScreen=False'
    okay_states = {'STARTING', 'ACTIVE'}
    if instance_id:
        lab_instance_url = '{0}/labapi/v1/instance?id={1}'.format(current_app.config['XTREME_URL'],
                                                                  instance_id)
        resp = requests.get(lab_instance_url, auth=HTTPBasicAuth(username=current_app.config['XTREME_ID'],
                                                                 password=current_app.config['XTREME_SECRET']))
        if resp.status_code != 200 or resp.json()['state'] not in okay_states:
            url = ''
        else:
            url = resp.json()['connectionUrl'] or url_base.format(current_app.config['XTREME_URL'], instance_id)
    else:
        payload = {
            'labID': lab_id
        }
        lab_url = '{0}/labapi/v1/Create'.format(current_app.config['XTREME_URL'])
        resp = requests.put(lab_url, json=payload, auth=HTTPBasicAuth(username=current_app.config['XTREME_ID'],
                                                                      password=current_app.config['XTREME_SECRET']))
        if resp.status_code != 200:
            url = ''
        else:
            lab_instance_id = resp.json()['id']
            redis_store.setex(response_id, 3600, lab_instance_id)
            url = url_base.format(current_app.config['XTREME_URL'], lab_instance_id)
    return render_template('xtreme.html', url=url)


@xtreme_bp.route('/submit', methods=['POST'])
def submit(token):
    try:
        lab_id, instance_id = external_serializer.loads(token, max_age=60)
    except (BadSignature, SignatureExpired):
        abort(400)