from .common import *

import django_heroku

ALLOWED_HOSTS = ["trocgraines.herokuapp.com"]

DEBUG = True

# Activate Django-Heroku.
django_heroku.settings(locals())
