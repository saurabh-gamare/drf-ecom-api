# Generated by Django 4.1 on 2023-09-12 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('category_image', models.URLField()),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_desc', models.TextField()),
                ('brand_name', models.CharField(max_length=50)),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=4)),
                ('discount_percent', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('stock_qty', models.IntegerField(default=0)),
                ('product_image', models.URLField()),
                ('size', models.CharField(max_length=50)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
        ),
    ]
