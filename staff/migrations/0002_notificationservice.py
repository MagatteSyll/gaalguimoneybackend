# Generated by Django 3.2.13 on 2022-09-16 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20220916_2219'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.service')),
            ],
        ),
    ]
