from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_image = models.URLField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand_name = models.CharField(max_length=50, default='ECOM')
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_qty = models.IntegerField(default=20)
    product_image = models.URLField()
    size = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=50, default='India')
    expiry_date = models.CharField(max_length=100, default='Please refer to the packaging of the product for expiry date.')
    customer_care = models.CharField(max_length=50, default='sgamare32@gmail.com')
    seller = models.CharField(max_length=50, default='Saurabh Gamare Ventures LLP')
    fssai = models.CharField(max_length=50, default='1234567890')

    @property
    def sale_price(self):
        discount_price = (float(self.mrp) * float(self.discount_percent)) / 100
        return '%.2f' % (float(self.mrp) - discount_price)

    def __str__(self):
        return self.product_name




