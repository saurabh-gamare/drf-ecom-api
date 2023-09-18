from django.urls import path
from . import views


urlpatterns = [
    path('coupon-list', views.CouponList.as_view(), name='coupon-list'),
    path('cart-detail', views.CartDetail.as_view(), name='cart-detail'),
    path('address-list-create', views.AddressCreateListMixin.as_view(), name='address-list-create'),
    path('address-retrieve-update-destroy/<int:pk>', views.AddressRetrieveUpdateDestroyMixin.as_view(), name='address-retrieve-update-destroy'),
]