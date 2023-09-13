from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path('auth', views.Auth.as_view(), name='auth'),
    path('login', views.Login.as_view(), name='login'),
    path('refresh-token', TokenRefreshView.as_view(), name='refresh-token'),
]