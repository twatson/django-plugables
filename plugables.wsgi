# Establish the enviornment
import os, os.path, sys
if not os.path.dirname(__file__) in sys.path[:1]:
    sys.path.insert(0, os.path.dirname(__file__))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Launch the project!
from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()