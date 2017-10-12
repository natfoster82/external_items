import os


SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
API_TOKEN = os.environ.get('AUTH_TOKEN', 'devtoken')
SEI_URL_BASE = os.environ.get('SEI_URL_BASE', 'https://sei.caveon.com')
SEI_ID = os.environ.get('SEI_ID')
SEI_SECRET = os.environ.get('SEI_SECRET')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

XTREME_URL = os.environ.get('XTREME_URL', 'https://uat.xtremeconsulting.com')
XTREME_ID = os.environ.get('XTREME_ID', '')
XTREME_SECRET = os.environ.get('XTREME_SECRET', '')
XTREME_ACCESS_CODE = os.environ.get('XTREME_ACCESS_CODE')
