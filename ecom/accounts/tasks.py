from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_async_otp_email(**kwargs):
    message = ''
    sender_email = settings.EMAIL_HOST_USER
    receiver_emails = [kwargs.get('receiver_email')]
    html_message = kwargs.get('html_message')
    send_mail(kwargs.get('subject'), message, sender_email, receiver_emails, html_message=html_message)
    return 'OTP Email Sent'

