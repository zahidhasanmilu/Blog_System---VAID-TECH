import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog_System.settings')

app = Celery('Blog_System')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
