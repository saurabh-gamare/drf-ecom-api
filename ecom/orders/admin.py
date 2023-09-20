from django.contrib import admin
from . import models


class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'status', 'total_payable', 'created_on')


admin.site.register(models.Order, OrderModelAdmin)
admin.site.register(models.OrderItem)