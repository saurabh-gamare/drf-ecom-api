# Generated by Django 4.1 on 2023-09-15 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_title', models.CharField(max_length=50)),
                ('coupon_description', models.CharField(max_length=100)),
                ('coupon_code', models.CharField(max_length=50)),
                ('flat_discount', models.IntegerField(blank=True, null=True)),
                ('min_cart_value', models.IntegerField(blank=True, null=True)),
                ('discount_percent', models.IntegerField(blank=True, null=True)),
                ('offer_cap', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
