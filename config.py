import os
from json import loads


SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
API_TOKEN = os.environ.get('AUTH_TOKEN', 'devtoken')
