import os, sys

sys.path.append('/home/plugables/applications')
sys.path.append('/home/plugables/applications/core')
sys.path.append('/home/plugables/applications/projects')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# def application(environ, start_response):
#     environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
#     return _application(environ, start_response)