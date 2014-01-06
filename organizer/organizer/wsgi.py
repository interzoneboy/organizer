"""
WSGI config for organizer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
import site

# Add the site-packages of this virtualenv
site.addsitedir("/home/matt/Code/Tools/organizer/lib/python2.7/site-packages")

# Add this app's directory to the PYTHONPATH
sys.path.append('/home/matt/Code/Tools/organizer')
sys.path.append('/home/matt/Code/Tools/organizer/organizer')
sys.path.append('/home/matt/Code/Tools/organizel/organizer/organizer')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "organizer.settings")

activate_env = os.path.expanduser("/home/matt/Code/Tools/organizer/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
