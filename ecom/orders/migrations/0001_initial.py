# Generated by Django 4.1 on 2023-09-19 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0020_alter_address_mobile_number_alter_address_pincode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=15)),
                ('status', models.CharField(choices=[('1', 'Processing'), ('2', 'Packing'), ('3', 'Packed'), ('4', 'Out For Delivery'), ('5', 'Delivered')], default='1', max_length=1)),
                ('coupon', models.CharField(max_length=15, null=True)),
                ('coupon_discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('total_mrp', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_sale_price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('delivery_fee', models.IntegerField()),
                ('total_payable', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('address_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cart.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
