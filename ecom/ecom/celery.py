import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom.settings')
app = Celery('ecom')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'sales-report-everyday': {
        'task': 'reports.tasks.send_sales_report',
        'schedule': crontab(hour='1', minute='5'),
    }
}
