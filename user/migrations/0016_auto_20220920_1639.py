# Generated by Django 3.2.13 on 2022-09-20 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20220917_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationtransaction',
            name='pays_reception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.pays'),
        ),
        migrations.AddField(
            model_name='viacode',
            name='pays_reception',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='user.pays'),
        ),
    ]
