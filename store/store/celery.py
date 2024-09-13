import os

from django.conf import settings
from celery import Celery




# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')