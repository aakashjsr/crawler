import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crawler.settings')

celery_app = Celery('crawler')
celery_app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()