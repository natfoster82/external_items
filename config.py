import os
from json import loads


SECRET_KEY = os.environ.get('SECRET_KEY', 'devkey')
