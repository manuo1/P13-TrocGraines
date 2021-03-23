from .common import *

import django_heroku

ALLOWED_HOSTS = ["trocgraines.herokuapp.com"]

DEBUG = False

# Activate Django-Heroku.
django_heroku.settings(locals())

INSTALLED_APPS += 'cloudinary_storage'
INSTALLED_APPS += 'cloudinary'

CLOUDINARY_STORAGE = {
	     'CLOUD_NAME': os.environ['CLOUDINARY_CLOUD_NAME'],
	     'API_KEY': os.environ['CLOUDINARY_API_KEY'],
	     'API_SECRET': os.environ['CLOUDINARY_API_SECRET']
	    }

DEFAULT_FILE_STORAGE='cloudinary_storage.storage.MediaCloudinaryStorage'
