from django.urls import path
from . import views


urlpatterns = [
    path('product-list', views.ProductList.as_view(), name='product-list'),
]