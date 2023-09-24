from django.urls import path
from . import views


urlpatterns = [
    path('sales-report', views.SalesReport.as_view(), name='sales-report'),
]