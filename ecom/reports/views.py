from django.shortcuts import render
from rest_framework.views import APIView
from orders.models import Order
from datetime import datetime, timedelta
from rest_framework.response import Response
from django.db.models import Sum
from .report import get_html_report
from io import BytesIO
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.conf import settings


class SalesReport(APIView):

    def convert_html_to_pdf(self, html_content):
        pdf_buffer = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_content.encode("UTF-8")), pdf_buffer)
        if not pdf.err:
            return pdf_buffer
        return None

    def get_datetime_x_days_ago(self, days):
        return (datetime.now() - timedelta(days=days)).replace(hour=0, minute=0, second=0)

    def get_last_and_prev_month_datetime(self):
        current_datetime = datetime.now()
        first_day_current_month = datetime(current_datetime.year, current_datetime.month, 1, 0, 0, 0)
        first_day_next_month = datetime(current_datetime.year, current_datetime.month + 1, 1)
        last_day_current_month = first_day_next_month - timedelta(days=1)
        return first_day_current_month, last_day_current_month

    def get_order_details(self, date1, date2):
        order_details = Order.objects.filter(created_on__gte=date1, created_on__lte=date2)
        return order_details

    def send_report_email(self, report_details):
        html_content = get_html_report(report_details)
        pdf_buffer = self.convert_html_to_pdf(html_content)
        if not pdf_buffer:
            return None
        subject = f'Sales Report <{report_details.get("current_date")}>'
        message = 'Please get the sales report attached.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['sgamare32@gmail.com']
        email = EmailMessage(subject, message, from_email, recipient_list)
        email.attach("sales_report.pdf", pdf_buffer.getvalue(), "application/pdf")
        email.send()

    def get(self, request):
        date_yesterday = self.get_datetime_x_days_ago(1)
        date_today = self.get_datetime_x_days_ago(0)
        orders_yesterday_instance = self.get_order_details(date_yesterday, date_today)
        orders_yesterday = len(orders_yesterday_instance)
        revenue_yesterday = orders_yesterday_instance.aggregate(total_payable=Sum('total_payable'))['total_payable']
        first_day_previous_month, last_day_previous_month = self.get_last_and_prev_month_datetime()
        orders_this_month_instance = self.get_order_details(first_day_previous_month, last_day_previous_month)
        orders_this_month = len(orders_this_month_instance)
        revenue_this_month = orders_this_month_instance.aggregate(total_payable=Sum('total_payable'))['total_payable']
        total_customers = Order.objects.values('user').distinct().count()
        current_date = datetime.now().strftime("%Y-%m-%d")
        report_details = {
            'orders_yesterday': orders_yesterday,
            'revenue_yesterday': round(revenue_yesterday, 2),
            'orders_this_month': orders_this_month,
            'revenue_this_month': round(revenue_this_month, 2),
            'total_customers': total_customers,
            'current_date': current_date
        }
        self.send_report_email(report_details)
        return Response(report_details)
