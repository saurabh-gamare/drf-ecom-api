# Generated by Django 4.0.4 on 2023-09-24 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_orderitem_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='coupon',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
