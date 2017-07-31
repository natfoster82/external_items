import os
from json import loads


SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
API_TOKEN = os.environ.get('AUTH_TOKEN', 'devtoken')
SEI_URL_BASE = os.environ.get('SEI_URL_BASE', 'https://sei.caveon.com')
SEI_ID = os.environ.get('SEI_ID')
SEI_SECRET = os.environ.get('SEI_SECRET')
ROLE_SECRETS = loads(os.environ.get('ROLE_SECRETS', '{}'))