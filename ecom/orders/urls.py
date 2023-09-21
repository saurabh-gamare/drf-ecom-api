from django.urls import path
from . import views


urlpatterns = [
    path('create-order', views.CreateOrder.as_view(), name='create-order'),
    path('list-orders', views.ListOrders.as_view(), name='list-orders'),
    path('retrieve-order', views.RetrieveOrder.as_view(), name='retrieve-order'),
]