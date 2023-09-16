from django.urls import path
from . import views


urlpatterns = [
    path('coupon-list', views.CouponList.as_view(), name='coupon-list'),
    path('cart-detail', views.CartDetail.as_view(), name='cart-detail'),
]