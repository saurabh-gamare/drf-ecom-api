from django.contrib import admin
from . import models


class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'mrp', 'sale_price', 'stock_qty')


admin.site.register(models.Product, ProductModelAdmin)
admin.site.register(models.Category)
