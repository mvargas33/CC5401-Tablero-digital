from .base import *

# Configurations for heroku:

import django_heroku
django_heroku.settings(locals())

# Not a real Heroku configuration, only for this project:
if os.environ.get('SINGLE_HEROKU_APP') == 'true':
    # Set directory to search for Vue index.html.
    TEMPLATES[0]['DIRS'].append(os.path.join(BASE_DIR, 'frontend/dist'))

    # Set directory from wich to collect Vue static resources.
    STATICFILES_DIRS.append(os.path.join(BASE_DIR, 'frontend/dist/static'))

DEBUG = False