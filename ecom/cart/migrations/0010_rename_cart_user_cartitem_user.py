# Generated by Django 4.1 on 2023-09-16 20:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_alter_cartitem_cart_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='cart_user',
            new_name='user',
        ),
    ]
