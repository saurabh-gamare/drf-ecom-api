from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class Coupon(models.Model):
    active = models.BooleanField(default=True)
    coupon_title = models.CharField(max_length=50, null=True, blank=True)
    coupon_description = models.CharField(max_length=100, null=True, blank=True)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)
    flat_discount = models.IntegerField(null=True, blank=True)
    min_cart_value = models.IntegerField(null=True, blank=True)
    discount_percent = models.IntegerField(null=True, blank=True)
    offer_cap = models.IntegerField(null=True, blank=True)
    coupon_usage = models.IntegerField(null=True, blank=True)

    def clean(self):
        if self.flat_discount and (self.discount_percent or self.offer_cap):
            raise ValidationError('Flat Discount, Discount Percent or Offer Cap cannot be added together')

    def __str__(self):
        return self.coupon_code


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)
    coupon_discount = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)
    total_mrp = models.DecimalField(max_digits=20, decimal_places=2)
    total_sale_price = models.DecimalField(max_digits=20, decimal_places=2)

    @property
    def delivery_fee(self):
        return 25 if self.total_sale_price < 199 else 0

    @property
    def total_payable(self):
        return float(self.total_sale_price) + float(self.delivery_fee) - float(self.coupon_discount)

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    user = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.user.username


class Address(models.Model):
    ADDRESS_LABEL_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=50)
    mobile_number = models.IntegerField()
    street_address_line_1 = models.CharField(max_length=255)
    street_address_line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    address_label = models.CharField(max_length=5, choices=ADDRESS_LABEL_CHOICES, default='home')

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.user.username
