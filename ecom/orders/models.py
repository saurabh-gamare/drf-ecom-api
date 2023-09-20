from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from cart.models import Address, Cart, CartItem
from django.utils import timezone
import random, string

User = get_user_model()


class Order(models.Model):
    STATUS_FIELD_CHOICES = [
        ('1', 'Processing'),
        ('2', 'Packing'),
        ('3', 'Packed'),
        ('4', 'Out For Delivery'),
        ('5', 'Delivered')
    ]
    # ALPHANUMERIC_STRING = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    order_id = models.CharField(max_length=15)
    status = models.CharField(max_length=1, choices=STATUS_FIELD_CHOICES, default='1')
    coupon = models.CharField(max_length=15, null=True)
    coupon_discount = models.DecimalField(default=0.0, max_digits=20, decimal_places=2)
    total_mrp = models.DecimalField(max_digits=20, decimal_places=2)
    total_sale_price = models.DecimalField(max_digits=20, decimal_places=2)
    delivery_fee = models.IntegerField()
    total_payable = models.DecimalField(max_digits=20, decimal_places=2)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # print(self.id, 'self.id')
        return self.order_id


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.order_id.order_id
