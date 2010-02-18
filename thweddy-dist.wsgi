import os
import sys

sys.stdout = sys.stderr


# Set up the environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'thweddy.settings'

BASE_DIR = ''
for path in (
	'thweddy',
	'thweddy.main',
	'thweddy/tweepy',
	'thweddy/django',
	):
    sys.path.append(os.path.join(BASE_DIR, path))


# Now the paths are set up we can load Django
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
