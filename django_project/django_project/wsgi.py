"""
WSGI config for django_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/

I could not make the global variables in this file prefixed with "g_"
because it would obstruct the functionality of certain components of
of this Django web application.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'django_project.settings')

application = get_wsgi_application()

# 6
