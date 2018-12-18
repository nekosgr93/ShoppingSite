import os

from .settings import *

DEBUG = False

ALLOWED_HOSTS = [
    'shopping-deploy.appspot.com',
    '127.0.0.1'
]

KEY_PATH = os.path.join(BASE_DIR, 'SECRET_KEY.txt')
with open(KEY_PATH) as f:
    SECRET_KEY = f.read().strip()

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_BUCKET_NAME = 'shopping-deploy'
GS_PROJECT_ID = 'shopping-deploy'

DATABASES = {
    'default': {
        # If you are using Cloud SQL for MySQL rather than PostgreSQL, set
        # 'ENGINE': 'django.db.backends.mysql' instead of the following.
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'shopping-site',
        'USER': 'test',
        'PASSWORD': 'testpassword',
        # For MySQL, set 'PORT': '3306' instead of the following. Any Cloud
        # SQL Proxy instances running locally must also be set to tcp:3306.
        'PORT': '5432',
    }
}

DATABASES['default']['HOST'] = '/cloudsql/shopping-deploy:us-central1:shopping-site'
if os.getenv('GAE_INSTANCE'):
    pass
else:
    DATABASES['default']['HOST'] = '127.0.0.1'

STATIC_URL = 'https://storage.googleapis.com/shopping-deploy/static/'
