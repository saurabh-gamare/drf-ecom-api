# Generated by Django 4.1 on 2023-09-09 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_otp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
