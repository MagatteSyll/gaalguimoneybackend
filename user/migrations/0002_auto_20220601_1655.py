# Generated by Django 3.2.13 on 2022-06-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='envoi',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
        migrations.AddField(
            model_name='viacode',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19),
        ),
    ]