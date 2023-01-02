from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','ecommerce.settings')
app = Celery('ecommerce')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
# app.autodiscover_tasks()
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

## an example of actual tasks, but originl tasks will be found in the app folders' tasks.py files 
@app.task(bind=True)
def hello_world(self):
    print('Hello world!')

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')