# Generated by Django 3.2.13 on 2022-09-03 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20220901_0323'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhoneVerificationCode',
        ),
    ]
