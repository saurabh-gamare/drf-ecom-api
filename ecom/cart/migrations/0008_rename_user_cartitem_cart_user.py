# Generated by Django 4.1 on 2023-09-16 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_rename_cart_id_cartitem_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='user',
            new_name='cart_user',
        ),
    ]
