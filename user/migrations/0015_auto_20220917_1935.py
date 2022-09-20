# Generated by Django 3.2.13 on 2022-09-17 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_remove_user_devise'),
    ]

    operations = [
        migrations.AddField(
            model_name='depot',
            name='sommecoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='envoi',
            name='sommecoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='payementgaalgui',
            name='prixcoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='retrait',
            name='sommecoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='retraitcode',
            name='sommecoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='verificationtransaction',
            name='sommecoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
        migrations.AddField(
            model_name='viacode',
            name='sommecoteclient',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True),
        ),
    ]
