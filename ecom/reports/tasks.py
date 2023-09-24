from celery import shared_task
import requests
from ecom.config import Config


@shared_task
def send_sales_report():
    domain = Config.API_DOMAIN
    url = f'{domain}/api/v1/reports/sales-report'
    requests.get(url, headers={}, data='')
    return 'Sales Report Sent'
