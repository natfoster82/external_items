from flask import Blueprint, request, current_app, render_template, url_for, abort, redirect
import requests
from requests.auth import HTTPBasicAuth
from itsdangerous import BadSignature, SignatureExpired
from helpers import redis_store, external_serializer


xtreme_bp = Blueprint('xtreme', __name__, template_folder='templates', static_folder='static', url_prefix='/xtreme')


@xtreme_bp.route('/url/<lab_id>', methods=['POST'])
def url(lab_id):
    # TODO: strengthen this auth with a user system that has unique xtreme keys stored
    access_code = request.args.get('access_code')
    if access_code != current_app.config['XTREME_ACCESS_CODE']:
        abort(403)
    data = request.get_json() or request.form
    response_id = data.get('response_id')
    exam_id = data.get('exam_id')
    instance_id = redis_store.get(response_id)
    token = external_serializer.dumps([lab_id, instance_id, exam_id])
    return url_for('xtreme.lab', token=token)


@xtreme_bp.route('/<token>')
def lab(token):
    try:
        lab_id, instance_id, exam_id = external_serializer.loads(token, max_age=60)
    except (BadSignature, SignatureExpired):
        abort(403)

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
            abort(400)
        url = resp.json()['connectionUrl'] or url_base.format(current_app.config['XTREME_URL'], instance_id)
    else:
        payload = {
            'labID': lab_id
        }
        lab_url = '{0}/labapi/v1/Create'.format(current_app.config['XTREME_URL'])
        resp = requests.put(lab_url, json=payload, auth=HTTPBasicAuth(username=current_app.config['XTREME_ID'],
                                                                      password=current_app.config['XTREME_SECRET']))
        if resp.status_code != 200:
            abort(400)
        instance_id = resp.json()['id']
        redis_store.setex(response_id, 3600, instance_id)
        url = url_base.format(current_app.config['XTREME_URL'], instance_id)
    return render_template('xtreme.html', url=url, response_id=response_id, instance_id=instance_id, exam_id=exam_id)


@xtreme_bp.route('/submit', methods=['POST'])
def submit():
    instance_id = request.form.get('instance_id')
    response_id = request.form.get('response_id')
    exam_id = request.form.get('exam_id')
    score_url = '{0}/labapi/v1/ScoreLab?id={1}'.format(current_app.config['XTREME_URL'], instance_id)
    # TODO: async this one
    requests.get(score_url, auth=HTTPBasicAuth(username=current_app.config['XTREME_ID'],
                                               password=current_app.config['XTREME_SECRET']))

    url = current_app.config['SEI_URL_BASE'] + '/api/set_response/' + response_id
    json = {
        'value': request.form['submit']
    }
    if exam_id and exam_id in current_app.config['ROLE_SECRETS']:
        username = current_app.config['SEI_ID']
        password = current_app.config['SEI_SECRET']
        r = requests.post(url, json=json, auth=HTTPBasicAuth(username=username, password=password))
        # TODO use the integration system instead
    else:
        r = None
    if r and r.status_code not in {200, 201}:
        abort(400)
    return redirect(url_for('lab.thank_you'))


@xtreme_bp.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')
