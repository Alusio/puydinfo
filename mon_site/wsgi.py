"""
WSGI config for mon_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import sys

import os
from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/puydinfo/mon_site')
sys.path.append('/var/www/puydinfo')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mon_site.settings')

application = get_wsgi_application()
