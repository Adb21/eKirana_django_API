import os

import sys

import site

from django.core.wsgi import get_wsgi_application

# Add the app’s directory to the PYTHONPATH

sys.path.append("C:/Users/bhosl/Desktop/Aditya_SSD/django Project/eKirana")

sys.path.append("C:/Users/bhosl/Desktop/Aditya_SSD/django Project/eKirana/eKirana")

os.environ['DJANGO_SETTINGS_MODULE'] = 'eKirana.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eKirana.settings')

application = get_wsgi_application()

