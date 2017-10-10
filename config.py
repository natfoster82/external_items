import os
from json import loads


SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
API_TOKEN = os.environ.get('AUTH_TOKEN', 'devtoken')
SEI_URL_BASE = os.environ.get('SEI_URL_BASE', 'https://sei.caveon.com')
SEI_ID = os.environ.get('SEI_ID')
SEI_SECRET = os.environ.get('SEI_SECRET')
ROLE_SECRETS = loads(os.environ.get('ROLE_SECRETS', '{}'))
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_ECHO = loads(os.environ.get('SQLALCHEMY_ECHO', 'false'))
SQLALCHEMY_TRACK_MODIFICATIONS = loads(os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS', 'false'))
SQLALCHEMY_POOL_SIZE = loads(os.environ.get('SQLALCHEMY_POOL_SIZE', '5'))

XTREME_URL = os.environ.get('XTREME_URL', 'https://uat.xtremeconsulting.com')
XTREME_ID = os.environ.get('XTREME_ID', '')
XTREME_SECRET = os.environ.get('XTREME_SECRET', '')